import pandas as pd
import os
import cx_Oracle
import pyodbc
import datacompy


class ConfigLoader:
    @staticmethod
    def read_config(config_path):
        return pd.read_excel(config_path)


class DBConnector:
    @staticmethod
    def connect_to_oracle(username, password, host, port, service_name):
        try:
            dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
            return connection
        except Exception as exp:
            print(f"Unable to connect to Oracle: {exp}")
            return None

    @staticmethod
    def connect_to_mssql(username, password, host, port, database):
        try:
            conn_str = f'DRIVER={{SQL Server}};SERVER={host},{port};DATABASE={database};UID={username};PWD={password}'
            connection = pyodbc.connect(conn_str)
            return connection
        except Exception as exp:
            print(f"Unable to connect to MSSQL: {exp}")
            return None


class DataFetcher:
    @staticmethod
    def fetch_data(source_config):
        if source_config['source_type'] == 'File':
            return pd.read_csv(source_config['source_detail'])
        elif source_config['source_type'] == 'Database':
            conn = None
            if source_config['source_db_type'] == 'Oracle':
                conn = DBConnector.connect_to_oracle(
                    source_config['source_user'], source_config['source_password'],
                    source_config['source_host'], source_config['source_port'], source_config['source_database']
                )
            elif source_config['source_db_type'] == 'MSSQL':
                conn = DBConnector.connect_to_mssql(
                    source_config['source_user'], source_config['source_password'],
                    source_config['source_host'], source_config['source_port'], source_config['source_database']
                )

            if conn:
                with open(source_config['source_query_file'], 'r') as f:
                    query = f.read()
                return pd.read_sql(query, conn)
        return None


class ReconEngine:
    def __init__(self, config):
        self.config = config
        self.source_data = DataFetcher.fetch_data(self.config)
        self.target_data = DataFetcher.fetch_data(self.config)

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
    config_df = ConfigLoader.read_config(file_path)

    for _, row in config_df.iterrows():
        config = {
            'source_name': row['Source Name'],
            'source_type': row['Source Type'],
            'source_detail': row['Source Detail'],
            'source_db_type': row['Source DB Type'],
            'source_host': row['Source Host'],
            'source_port': row['Source Port'],
            'source_database': row['Source Database'],
            'source_user': row['Source User ID'],
            'source_password': row['Source Password'],
            'source_query_file': row['Source Query File'],
            'target_name': row['Target Name'],
            'target_type': row['Target Type'],
            'target_detail': row['Target Detail'],
            'target_db_type': row['Target DB Type'],
            'target_host': row['Target Host'],
            'target_port': row['Target Port'],
            'target_database': row['Target Database'],
            'target_user': row['Target User ID'],
            'target_password': row['Target Password'],
            'target_query_file': row['Target Query File'],
            'comparison_keys': row['Comparison Keys'].split(',')
        }

        recon_engine = ReconEngine(config)
        recon_engine.run_recon()

    print('## Recon Completed...! ##')