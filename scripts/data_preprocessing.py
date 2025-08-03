import pandas as pd
import numpy as np
import os

def load_and_clean_data(input_path, output_path):
    """Load and clean Brent oil price data."""
    data = pd.read_csv(input_path)
    data['Date'] = pd.to_datetime(data['Date'], format='mixed')
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    data['Date'] = pd.to_datetime(data['Date'])

    print("Initial Duplicate Rows:", data.duplicated().sum())
    print("Duplicate Dates:", data['Date'].duplicated().sum())

    data = data.drop_duplicates(subset=['Date'], keep='first')
    print("Rows After Deduplication:", len(data))

    print("Missing Values:", data.isnull().sum())

    data.set_index('Date', inplace=True)
    data.to_csv(output_path)
    return data

def compute_log_returns(data, output_path):
    """Compute log returns and save to CSV."""
    data['Log_Returns'] = np.log(data['Price']).diff()
    data[['Log_Returns']].to_csv(output_path)
    return data

if __name__ == "__main__":
    os.makedirs('data/processed', exist_ok=True)

    raw_data_path = 'data/raw/BrentOilPrices.csv'
    cleaned_data_path = 'data/processed/brent_oil_prices_cleaned.csv'
    log_returns_path = 'data/processed/log_returns.csv'

    data = load_and_clean_data(raw_data_path, cleaned_data_path)
    data = compute_log_returns(data, log_returns_path)
