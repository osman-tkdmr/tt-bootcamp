import duckdb
import os
import requests
import gzip
import shutil
from tqdm import tqdm

DATA_FOLDER = "../Data"
os.makedirs(DATA_FOLDER, exist_ok=True)

urls = [
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.1.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.2.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.3.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.4.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.5.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.6.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.7.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.8.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.9.jsonl.gz",
    "https://storage.googleapis.com/sadedegel/dataset/tt-capstone/capstone.10.jsonl.gz"
]

def download_file(url, folder=DATA_FOLDER):
    """Dosyayı URL'den indirir ve kaydeder."""
    local_filename = os.path.join(folder, url.split("/")[-1])
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    
    with open(local_filename, "wb") as file, tqdm(
        desc=f"İndiriliyor: {local_filename}",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(1024):
            file.write(data)
            bar.update(len(data))
    
    return local_filename

def extract_gz_file(filepath, extract_to=DATA_FOLDER):
    """`.jsonl.gz` dosyasını açar ve `.jsonl` olarak kaydeder."""
    if not filepath.endswith(".jsonl.gz"):
        print(f"⚠ Desteklenmeyen dosya formatı: {filepath}")
        return
    
    extracted_filepath = os.path.join(extract_to, os.path.basename(filepath).replace(".gz", ""))
    
    with gzip.open(filepath, "rb") as gz_file, open(extracted_filepath, "wb") as out_file:
        shutil.copyfileobj(gz_file, out_file)

    print(f"✅ Çıkartıldı: {extracted_filepath}")
    os.remove(filepath)  

for url in urls:
    try:
        file_path = download_file(url)
        extract_gz_file(file_path)
    except Exception as e:
        print(f"Hata oluştu: {e}")