# Dataset Setup

## Olist Brazilian E-Commerce Dataset

This project uses the Olist dataset from Kaggle containing 100,000 orders from 2016-2018.

### Option 1: Automatic Download (Recommended)

```bash
# Install Kaggle CLI
pip install kaggle

# Set up Kaggle API credentials
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token"
# 3. Save kaggle.json to ~/.kaggle/kaggle.json
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
python src/download_dataset.py
```

### Option 2: Manual Download

1. Visit: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Click "Download" (requires Kaggle account)
3. Extract all CSV files to `data/raw/` folder
4. Run: `python src/setup_database.py`

## Dataset Tables

The dataset includes 9 interconnected tables:

1. **orders** - Order information
2. **order_items** - Items in each order
3. **order_payments** - Payment details
4. **order_reviews** - Customer reviews
5. **customers** - Customer data
6. **products** - Product catalog
7. **sellers** - Seller information
8. **geolocation** - Location coordinates
9. **product_category_name_translation** - Category translations

All tables will be automatically loaded into SQLite database: `ecommerce.db`
