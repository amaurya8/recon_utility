import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from io import BytesIO
pip install azure-storage-file-datalake pandas pyarrow
def fetch_adls_folder_to_df(account_name: str, account_key: str, file_system: str, folder_path: str, file_type: str = "csv") -> pd.DataFrame:
    try:
        service_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net",
            credential=account_key
        )

        file_system_client = service_client.get_file_system_client(file_system)
        paths = file_system_client.get_paths(path=folder_path)

        all_dfs = []

        for path in paths:
            if not path.is_directory:
                file_client = file_system_client.get_file_client(path.name)
                download = file_client.download_file()
                file_content = BytesIO(download.readall())

                if file_type == "csv":
                    df = pd.read_csv(file_content)
                elif file_type == "json":
                    df = pd.read_json(file_content, lines=True)
                elif file_type == "parquet":
                    df = pd.read_parquet(file_content)
                else:
                    raise ValueError(f"Unsupported file type: {file_type}")

                all_dfs.append(df)

        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            return combined_df
        else:
            print("No files found in folder.")
            return pd.DataFrame()

    except Exception as e:
        print(f"Error reading files from ADLS folder: {e}")
        return pd.DataFrame()