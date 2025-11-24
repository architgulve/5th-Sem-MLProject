import os
import requests
import zipfile
from io import BytesIO

OUT_DIR = "../data/raw"
URL = "https://analyse.kmi.open.ac.uk/open_dataset"  # page; direct download link available on that page

def download_oulad_zip(download_url, out_dir=OUT_DIR):
    os.makedirs(out_dir, exist_ok=True)
    print("Please download OULAD zip from the official page and place it in data/raw, or run this script with a direct zip link.")
    print("OULAD info / download page: https://analyse.kmi.open.ac.uk/open_dataset")
    # The site hosts a download link; in many environments you must click-to-download (or use wget with the zip's url).
    # For reproducibility, I recommend manually downloading the zip from the above page into data/raw/.

if __name__ == "__main__":
    download_oulad_zip(URL)
