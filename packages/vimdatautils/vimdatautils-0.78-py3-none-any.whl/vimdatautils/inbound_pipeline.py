import datetime
import os
from jinja2 import Template
from abc import ABC, abstractmethod
from .s3_utility import S3Utility
from .dal import Dal


class InboundPipeline(ABC):
    """
        InboundPipeline
        Args:
            config_file: full file path for config file
            postgres_connection_string: local example, "postgresql://postgres:password@127.0.0.1/postgres"
    """

    def __init__(self, config_obj, scripts_location, postgres_connection_string):
        self.table_stats = dict()
        self.scripts_location = scripts_location
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.sync_date = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self.config = config_obj
        self.dal = Dal(postgres_connection_string)
        self.aws = S3Utility()

    @abstractmethod
    def pre_load_logic(self):
        pass

    @abstractmethod
    def post_load_logic(self):
        pass

    def execute(self):
        """
            Executing the pipeline
            1. Deployed depended resources on the database
            2. Downloading files from s3
            3. Executing provided pre load logic
            4. Loading data to the database
            5. Executing provided post load logic
            6. Renaming the tables (switch tables)
            7. Updating logs
        """
        try:
            self.dal.execute_file(os.path.join(self.directory, 'resources', 'create_inbound_stored_functions.sql'))
            self.dal.execute_file(os.path.join(self.directory, 'resources', 'update_log_table.sql'))
            self.download_files(self.config.download_s3_files)
            self.pre_load_logic()
            self.load_data(self.config.local_dir, self.config.tables_to_load, self.scripts_location, self.sync_date)
            self.post_load_logic()
            self.rename_tables(self.sync_date, self.config.tables_to_load)
            self.update_log(self.config.tables_to_load)
        finally:
            self.cleanup(self.config, self.sync_date)
            self.dal.close()

    def download_files(self, download_s3_files):
        for file in download_s3_files:
            self.aws.download_latest_file(file.s3_bucket, file.regex, os.path.join(self.config.local_dir, file.file_name))

    def load_data(self, local_dir, tables_config, scripts_location, sync_date):
        for table_config in tables_config:
            full_path_file = os.path.join(local_dir, table_config.file_name)
            if os.path.isfile(full_path_file):
                if table_config.ddl_script:
                    ddl_file_location = os.path.join(scripts_location, table_config.ddl_script)
                    self.execute_jinja_file(ddl_file_location, {'sync_date': sync_date})
                    table_name = self.generate_table_name(sync_date, table_config)
                    row_count = self.dal.copy_to_table(table_name, full_path_file, table_config.has_headers, table_config.is_csv_format,
                                                       table_config.delimiter, table_config.empty_string, table_config.black_columns_list,
                                                       table_schema=table_config.table_schema)
                    self.table_stats[table_config.table_name] = {'row_count': row_count, 'file_name': table_config.file_name}

    def update_log(self, tables):
        for table in tables:
            if table.table_name in self.table_stats:
                query = f"insert into update_log(table_name, entities_count) values( %s , %s);"
                self.dal.execute_cmd(query, (table.table_name, self.table_stats[table.table_name]['row_count'],))

    # Dropping tables, deleting directory
    def cleanup(self, conf, sync_date):
        for table in conf.tables_to_load:
            table_name = self.generate_table_name(sync_date, table)
            self.dal.execute_cmd(f"drop table if exists {table.table_schema}.{table_name};")
        os.system(f"rm -Rf {conf.local_dir}")

    @staticmethod
    def generate_table_name(sync_date, table):
        return table.table_name if table.is_delta else f'{table.table_name}{sync_date}'

    def execute_jinja_file(self, template_path, keywords):
        with open(template_path, "r") as file:
            data = file.read()
        file.close()
        sql = str(Template(data).render(keywords=keywords))
        self.dal.execute_cmd(sql)

    def rename_tables(self, sync_date, tables):
        for table in tables:
            if not table.is_delta and table.table_name in self.table_stats:
                ARCHIVE_SUFFIX = "old"
                source_table_name = f"{table.table_name}{sync_date}"
                self.dal.switch_tables(table.table_schema, source_table_name, table.table_name, ARCHIVE_SUFFIX)
