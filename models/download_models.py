#!/usr/bin/env python3

import hashlib
import os
import sys
from pathlib import Path
import requests
from tqdm import tqdm
import yaml

# Constants
MODELS_DIR = Path(__file__).parent
CONFIG_FILE = MODELS_DIR / "model_config.yml"
CHUNK_SIZE = 8192

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_file(url, local_path, expected_hash=None):
    """Download a file with progress bar and optional hash verification."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(local_path, 'wb') as f, tqdm(
            desc=local_path.name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(CHUNK_SIZE):
                size = f.write(data)
                pbar.update(size)
        
        if expected_hash:
            actual_hash = calculate_sha256(local_path)
            if actual_hash != expected_hash:
                print(f"❌ Hash mismatch for {local_path}")
                print(f"Expected: {expected_hash}")
                print(f"Got: {actual_hash}")
                os.remove(local_path)
                return False
        return True
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        if local_path.exists():
            os.remove(local_path)
        return False

def main():
    """Main function to download and verify models."""
    if not CONFIG_FILE.exists():
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    
    models_to_download = config.get('models', {})
    if not models_to_download:
        print("❌ No models specified in config file")
        sys.exit(1)
    
    print("🔄 Starting model downloads...")
    success = True
    
    for model_name, model_info in models_to_download.items():
        model_path = MODELS_DIR / model_name
        
        if model_path.exists():
            if 'sha256' in model_info:
                current_hash = calculate_sha256(model_path)
                if current_hash == model_info['sha256']:
                    print(f"✅ {model_name} already exists and hash matches")
                    continue
            else:
                print(f"⚠️ {model_name} exists but no hash to verify")
                continue
        
        print(f"\n📥 Downloading {model_name}...")
        if not download_file(
            model_info['url'],
            model_path,
            model_info.get('sha256')
        ):
            success = False
    
    if success:
        print("\n✅ All models downloaded and verified successfully!")
    else:
        print("\n❌ Some downloads failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 