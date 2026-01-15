"""
Download Olist Brazilian E-Commerce dataset from Kaggle
"""
import os
import sys
import zipfile
from pathlib import Path

def download_dataset():
    """Download the Olist dataset from Kaggle"""

    # Check if kaggle is installed
    try:
        import kaggle
    except ImportError:
        print("❌ Kaggle package not found. Install it with: pip install kaggle")
        sys.exit(1)

    # Create data directories
    data_dir = Path(__file__).parent.parent / "data"
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Check for Kaggle credentials
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("❌ Kaggle credentials not found!")
        print("\nSetup instructions:")
        print("1. Go to https://www.kaggle.com/settings")
        print("2. Click 'Create New API Token'")
        print("3. Save kaggle.json to ~/.kaggle/kaggle.json")
        print("4. Run: chmod 600 ~/.kaggle/kaggle.json")
        sys.exit(1)

    print("📦 Downloading Olist Brazilian E-Commerce dataset...")
    print("This may take a few minutes...\n")

    try:
        # Download dataset
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()

        dataset = "olistbr/brazilian-ecommerce"
        api.dataset_download_files(dataset, path=raw_dir, unzip=True)

        print("✅ Dataset downloaded successfully!")
        print(f"📁 Location: {raw_dir}")

        # List downloaded files
        csv_files = list(raw_dir.glob("*.csv"))
        print(f"\n📊 Found {len(csv_files)} CSV files:")
        for f in sorted(csv_files):
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name} ({size_mb:.2f} MB)")

        print("\n✨ Next step: Run 'python src/setup_database.py' to create the database")

    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\nTry manual download:")
        print("1. Visit: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
        print(f"2. Download and extract to: {raw_dir}")
        sys.exit(1)

if __name__ == "__main__":
    download_dataset()
