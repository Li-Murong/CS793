import os
import requests
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

subdir = 'data'
if not os.path.exists(subdir):
    os.makedirs(subdir)
subdir = subdir.replace('\\', '/')  # Compatible with Windows systems

# Configure retry strategy
session = requests.Session()
retries = Retry(
    total=5,  # Number of retries
    backoff_factor=0.5,  # Backoff factor for wait time
    status_forcelist=[500, 502, 503, 504],  # HTTP status codes to retry
)
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

for ds in [
    'webtext',
    'small-117M',
    'small-117M-k40',
    'medium-345M',
    'medium-345M-k40',
    'large-762M',
    'large-762M-k40',
    'xl-1542M',
    'xl-1542M-k40',
]:
    for split in ['train', 'valid', 'test']:
        filename = f"{ds}.{split}.jsonl"
        url = f"https://openaipublic.azureedge.net/gpt-2/output-dataset/v1/{filename}"
        filepath = os.path.join(subdir, filename)

        # Check if the file already exists
        if os.path.exists(filepath):
            print(f"File {filename} already exists, skipping download.")
            continue

        try:
            with session.get(url, stream=True, timeout=(5, 60)) as r:
                r.raise_for_status()  # Check if the request was successful
                file_size = int(r.headers.get("Content-Length", 0))
                chunk_size = 1024 * 1024  # 1 MB

                with open(filepath, 'wb') as f, tqdm(
                        desc=f"Fetching {filename}",
                        total=file_size,
                        unit='iB',
                        unit_scale=True,
                        unit_divisor=1024,
                        ncols=100,
                ) as pbar:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")
