import pandas as pd
from adlfs import AzureBlobFileSystem

def read_all_files_from_adls_folder_with_connection_string(
    connection_string, container_name, folder_path, file_type="csv"
):
    try:
        # Create the ADLS filesystem using connection string
        fs = AzureBlobFileSystem(connection_string=connection_string)

        # Clean up the path and list matching files
        folder_path = folder_path.strip("/")
        full_path = f"{container_name}/{folder_path}"
        file_list = fs.glob(f"{full_path}/*.{file_type}")

        if not file_list:
            print("No files found.")
            return pd.DataFrame()

        # Read and combine files
        dfs = []
        for file in file_list:
            with fs.open(file, "rb") as f:
                if file_type == "csv":
                    df = pd.read_csv(f)
                elif file_type == "parquet":
                    df = pd.read_parquet(f)
                else:
                    raise ValueError("Unsupported file type")
                dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    except Exception as e:
        print(f"Error reading files from ADLS: {e}")
        return pd.DataFrame()