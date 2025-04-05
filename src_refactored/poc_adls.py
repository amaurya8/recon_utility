import pandas as pd
import fsspec
from azure.identity import ClientSecretCredential

def read_all_files_from_adls_folder(
    storage_account, container_name, folder_path,
    tenant_id, client_id, client_secret,
    file_type="csv"  # can be 'csv' or 'parquet'
):
    try:
        # Authenticate using the service principal
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        # Create the filesystem
        fs = fsspec.filesystem("abfs", account_name=storage_account, credential=credential)

        # List all files in the folder
        full_folder_path = f"{container_name}/{folder_path}".rstrip("/")
        file_list = fs.glob(f"{full_folder_path}/*.{file_type}")

        if not file_list:
            print("No files found.")
            return pd.DataFrame()

        # Read and combine all files
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