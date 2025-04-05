import pandas as pd
import fsspec
from azure.identity import ClientSecretCredential

def read_all_files_from_adls_folder(
    storage_account, container_name, folder_path,
    tenant_id, client_id, client_secret,
    file_type="csv"  # can be 'csv' or 'parquet'
):
    try:
        print("Authenticating using service principal...")

        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        print(f"Creating filesystem for storage account: {storage_account}")
        fs = fsspec.filesystem("abfs", account_name=storage_account, credential=credential)

        folder_path = folder_path.strip("/")  # Clean up slashes
        abfs_path = f"abfs://{container_name}/{folder_path}"
        print(f"Looking for files at: {abfs_path}/*.{file_type}")

        file_list = fs.glob(f"{abfs_path}/*.{file_type}")
        print(f"Files found: {file_list}")

        if not file_list:
            print("⚠️ No files found. Double-check the path, container, or file type.")
            return pd.DataFrame()

        dataframes = []
        for file in file_list:
            print(f"Reading file: {file}")
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
        print(f"❌ Error reading folder from ADLS: {e}")
        return pd.DataFrame()