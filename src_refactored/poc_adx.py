from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
import pandas as pd
from azure.kusto.data.helpers import dataframe_from_result_table

def fetch_adx_data(cluster_uri: str, database: str, query: str, client_id: str, client_secret: str, authority_id: str) -> pd.DataFrame:
    try:
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster_uri, client_id, client_secret, authority_id
        )
        client = KustoClient(kcsb)
        response = client.execute(database, query)

        # Convert using helper
        df = dataframe_from_result_table(response.primary_results[0])
        return df

    except Exception as e:
        print(f"Error fetching data from ADX: {e}")
        return pd.DataFrame()