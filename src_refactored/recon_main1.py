import pandas as pd
import os
import cx_Oracle
import pyodbc
import datacompy

class DBConnector:
    @staticmethod
    def connect_to_oracle(username, password, host, port, service_name):
        try:
            dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
            return connection
        except Exception as exp:
            print(f"Unable to connect to Oracle: {exp}")

    @staticmethod
    def connect_to_mssql(username, password, host, port, database):
        try:
            conn_str = f'DRIVER={{SQL Server}};SERVER={host},{port};DATABASE={database};UID={username};PWD={password}'
            connection = pyodbc.connect(conn_str)
            return connection
        except Exception as exp:
            print(f"Unable to connect to MSSQL: {exp}")

class InitConfigs:
    def __init__(self, config_df):
        self.configs = []
        for _, row in config_df.iterrows():
            self.configs.append({
                'source_name': row['Source Name'],
                'source_type': row['Source Type'],
                'source_format': row['Source Format'],
                'source_detail': row['Source Detail'],
                'target_name': row['Target Name'],
                'target_type': row['Target Type'],
                'target_format': row['Target Format'],
                'target_detail': row['Target Detail'],
                'source_db_type': row['Source DB Type'],
                'source_host': row['Source Host'],
                'source_port': row['Source Port'],
                'source_database': row['Source Database'],
                'source_user': row['Source User ID'],
                'source_password': row['Source Password'],
                'source_query_file': row['Source Query File'],
                'target_db_type': row['Target DB Type'],
                'target_host': row['Target Host'],
                'target_port': row['Target Port'],
                'target_database': row['Target Database'],
                'target_user': row['Target User ID'],
                'target_password': row['Target Password'],
                'target_query_file': row['Target Query File'],
                'comparison_keys': row['Comparison Keys'].split(',')
            })

class ReconEngine:
    def __init__(self, config):
        self.config = config
        self.source_data = self.load_source_data()
        self.target_data = self.load_target_data()

    def load_source_data(self):
        if self.config['source_type'] == 'File':
            return pd.read_csv(self.config['source_detail'])
        elif self.config['source_type'] == 'Database':
            if self.config['source_db_type'] == 'Oracle':
                conn = DBConnector.connect_to_oracle(
                    self.config['source_user'],
                    self.config['source_password'],
                    self.config['source_host'],
                    self.config['source_port'],
                    self.config['source_database']
                )
            elif self.config['source_db_type'] == 'MSSQL':
                conn = DBConnector.connect_to_mssql(
                    self.config['source_user'],
                    self.config['source_password'],
                    self.config['source_host'],
                    self.config['source_port'],
                    self.config['source_database']
                )
            with open(self.config['source_query_file'], 'r') as f:
                query = f.read()
            return pd.read_sql(query, conn)

    def load_target_data(self):
        if self.config['target_type'] == 'File':
            return pd.read_csv(self.config['target_detail'])
        elif self.config['target_type'] == 'Database':
            if self.config['target_db_type'] == 'Oracle':
                conn = DBConnector.connect_to_oracle(
                    self.config['target_user'],
                    self.config['target_password'],
                    self.config['target_host'],
                    self.config['target_port'],
                    self.config['target_database']
                )
            elif self.config['target_db_type'] == 'MSSQL':
                conn = DBConnector.connect_to_mssql(
                    self.config['target_user'],
                    self.config['target_password'],
                    self.config['target_host'],
                    self.config['target_port'],
                    self.config['target_database']
                )
            with open(self.config['target_query_file'], 'r') as f:
                query = f.read()
            return pd.read_sql(query, conn)

    def run_recon(self):
        comparison = datacompy.Compare(
            self.source_data, self.target_data,
            join_columns=self.config['comparison_keys']
        )
        print(comparison.report())

if __name__ == "__main__":
    print('## Starting Recon Engine...! ##')
    pd.set_option('display.max_columns', None)

    file_path = 'Driver_Config.xlsx'
    config_df = pd.read_excel(file_path)
    init_configs = InitConfigs(config_df)

    for config in init_configs.configs:
        recon_engine = ReconEngine(config)
        recon_engine.run_recon()

    print('## Recon Completed...! ##')
