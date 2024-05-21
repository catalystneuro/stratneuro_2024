from dandi.dandiapi import DandiAPIClient
import fsspec
import pynwb
import h5py
from fsspec.implementations.cached import CachingFileSystem
import requests
import os


def download_file(url, local_file_name):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(local_file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded successfully to {local_file_name}")
        else:
            print(f"Failed to download file. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_nwbfile(dandiset_id, dandiset_file_path, dandiset_token, local_file_name):
    api_kwargs = {
        "api_url": "https://api-staging.dandiarchive.org/api",
        "token": dandiset_token
    }
    with DandiAPIClient(**api_kwargs) as client:
        asset = client.get_dandiset(dandiset_id, 'draft').get_asset_by_path(dandiset_file_path)
        download_url = asset.base_download_url
    download_file(url=download_url, local_file_name=local_file_name)


def get_file_size_in_mb(file_path):
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
        return file_size_mb
    except OSError as e:
        raise FileNotFoundError(f"Error: {e}")

        
# # Download the file you previously uploaded to DANDI archive
# # Fill in the correct info for your file and api key
# dandiset_id="213840",
# dandiset_filepath="sub-id0123/sub-id0123_ses-id987_ecephys.nwb",
# dandiset_token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
# local_file_name=""

# download_nwbfile(
#     dandiset_id=dandiset_id,
#     dandiset_file_path=dandiset_file_path,
#     dandiset_token=dandiset_token,
#     local_file_name=local_file_name
# )

# # Alternative method
# from dandi.download import download

# download(
#     urls="https://api-staging.dandiarchive.org/api/assets/9e6c25a9-2e46-4ea6-9375-37d2639c219b/download/",
#     output_dir="."
# )