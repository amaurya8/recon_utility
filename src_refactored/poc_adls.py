import pandas as pd
from azure.identity import ClientSecretCredential
from adlfs import AzureBlobFileSystem
import fsspec

def read_all_files_from_adls_folder(
    storage_account, container_name, folder_path,
    tenant_id, client_id, client_secret,
    file_type="csv"  # can be 'csv' or 'parquet'
):
    try:
        # Create the service principal credential
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        # Use adlfs directly for AzureBlobFileSystem
        fs = AzureBlobFileSystem(
            account_name=storage_account,
            credential=credential
        )

        folder_path = folder_path.strip('/')
        full_path = f"{container_name}/{folder_path}"

        file_list = fs.glob(f"{full_path}/*.{file_type}")
        print(f"Found files: {file_list}")

        if not file_list:
            print("No files found.")
            return pd.DataFrame()

        dataframes = []
        for file in file_list:
            with fs.open(file, "rb") as f:
                if file_type == "csv":
                    df = pd.read_csv(f)
                elif file_type == "parquet":
                    df = pd.read_parquet(f)
                else:
                    raise ValueError("Unsupported file type")
                dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df

    except Exception as e:
        print(f"Error reading folder from ADLS: {e}")
        return pd.DataFrame()