from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
import cx_Oracle
import pandas as pd
import pyodbc
import psycopg2
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
import multipledispatch

class AzureDataExplorer:

    @staticmethod
    def query_adx_and_get_dataframe(cluster, database, client_id, client_secret, tenant_id, query):
        try:
            # Define the connection string
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                cluster, client_id, client_secret, tenant_id
            )
            # Create a Kusto client
            client = KustoClient(kcsb)
            # Query the data
            response = client.execute(database, query)
            # Convert response to DataFrame
            df = dataframe_from_result_table(response.primary_results[0])
            return df

        except KustoServiceError as error:
            print(f"Kusto service error: {error}")
            return None

    @staticmethod
    def get_kusto_client(cluster, database, client_id, client_secret, tenant_id, query):
        try:
            # Define the connection string
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                cluster, client_id, client_secret, tenant_id
            )
            # Create a Kusto client
            client = KustoClient(kcsb)
            return client
        except Exception as exp:
            print(f"Error Occurred while connecting to ADX: {exp}")

    @staticmethod
    def insert_data_from_csv_to_adx(cluster_name, region, database_name, client_id, client_secret, authority_id,
                                    table_name, csv_file_path):
        # Define the connection string
        cluster = f"https://{cluster_name}.{region}.kusto.windows.net"
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster, client_id, client_secret, authority_id
        )

        # Create a Kusto client
        client = KustoClient(kcsb)

        try:
            # Insert data from CSV file into ADX table
            client.execute_mgmt(database_name, f'.ingest inline into table {table_name} <| {csv_file_path} |>')

        except KustoServiceError as e:
            print(f"Error inserting data: {e}")


class Oracle:

    @staticmethod
    def connect_to_oracle(username, password, host, port, service_name):
        try:
            # Construct the connection string
            dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
            return connection
        except Exception as exp:
            print(f"Unable to connect to Oracle: {exp}")

    @staticmethod
    def query_from_oracle_to_dataframe(connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            # Get column names from the cursor description
            columns = [desc[0] for desc in cursor.description]
            # Create a DataFrame from the query result
            df = pd.DataFrame(rows, columns=columns)
            cursor.close()
            return df
        except Exception as exp:
            print(f"Exception occurred: {exp}")


class MSSQL:

    @staticmethod
    def query_from_mssql_to_dataframe(conn, query):
        try:
            # Create a cursor from the connection
            cursor = conn.cursor()

            # Execute the query and fetch data into a DataFrame
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

            # Close the cursor
            cursor.close()

            return df
        except Exception as exp:
            print(f"Error Occurred: {exp}")

    @staticmethod
    def connect(server, database, username, password):
        try:
            # Establish a connection to the database
            conn_str = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as exp:
            print(f"Error Occurred: {exp}")


class Postgres:

    @staticmethod
    def connect_to_postgres(host, port, database, user, password):
        try:
            conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
            return conn
        except Exception as e:
            print(f"Unable to connect to PostgreSQL: {e}")

    @staticmethod
    def query_from_postgres_to_dataframe(connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            cursor.close()
            return df
        except Exception as e:
            print(f"Error executing query: {e}")


# class DB2:
#
#     @staticmethod
#     def connect_to_db2(hostname, port, database, username, password):
#         try:
#             conn_str = f"DATABASE={database};HOSTNAME={hostname};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};"
#             conn = ibm_db.connect(conn_str, "", "")
#             return conn
#         except Exception as e:
#             print(f"Unable to connect to DB2: {e}")
#
#     @staticmethod
#     def query_to_dataframe(conn, query):
#         try:
#             stmt = ibm_db.exec_immediate(conn, query)
#             result = ibm_db.fetch_both(stmt)
#             rows = []
#             while result:
#                 rows.append(result.copy())
#                 result = ibm_db.fetch_both(stmt)
#             columns = [col[0] for col in ibm_db.fetch_tuple(stmt)]
#             df = pd.DataFrame(rows, columns=columns)
#             return df
#         except Exception as e:
#             print(f"Error executing query: {e}")


class AzureSQL:

    @staticmethod
    def connect_to_azuresql(server, database, username, password):
        try:
            conn_str = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};"
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Unable to connect to Azure SQL: {e}")

    @staticmethod
    def query_from_azsql_to_dataframe(conn, query):
        try:
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")


class CosmosDB:

    @staticmethod
    def connect_to_cosmosdb(endpoint, key, database_name, container_name):
        try:
            client = CosmosClient(endpoint, key)
            database = client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            return container
        except Exception as e:
            print(f"Unable to connect to Azure Cosmos DB: {e}")

    @staticmethod
    def query_to_dataframe(container, query):
        try:
            items = list(container.query_items(query=query, enable_cross_partition_query=True))
            df = pd.DataFrame(items)
            return df
        except Exception as e:
            print(f"Error querying data from Cosmos DB: {e}")


class ADLSGen2:

    @staticmethod
    def connect_to_adls(account_name):
        try:
            credential = DefaultAzureCredential()
            service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=credential)
            return service_client
        except Exception as e:
            print(f"Unable to connect to ADLS Gen2: {e}")

    @staticmethod
    def read_csv(service_client, file_system_name, file_path):
        try:
            file_system_client = service_client.get_file_system_client(file_system=file_system_name)
            file_client = file_system_client.get_file_client(file_path)
            data = file_client.download_file().readall().decode('utf-8')
            df = pd.read_csv(pd.compat.StringIO(data))
            return df
        except Exception as e:
            print(f"Error reading CSV file from ADLS Gen2: {e}")


    @staticmethod @multipledispatch
    def connect_to_adls(account_name, client_id, client_secret, authority_id):
        try:
            credential = ClientSecretCredential(authority=authority_id, client_id=client_id, client_secret=client_secret)
            service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=credential)
            return service_client
        except Exception as e:
            print(f"Unable to connect to ADLS Gen2: {e}")