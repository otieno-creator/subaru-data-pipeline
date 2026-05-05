"""
Subaru Market Data Pipeline
Author: Dan Otieno (AWS Security Champion)
Purpose: Demonstrates a resilient ETL pattern for processing marketplace data.
"""

import pandas as pd
import logging

# Configure structured logging to provide production observability
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleanses raw marketplace data using defensive programming.
    Handles non-numeric values and removes incomplete records to ensure data integrity.
    """
    logging.info("Initiating Data Transformation...")

    # Defensive Casting: Converts messy strings to numbers. 
    # Invalid entries (like 'N/A' or 'corrupt') are safely turned into NaN.
    df['Price_KSh'] = pd.to_numeric(df['Price_KSh'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Data Validation: Drop rows where Price is missing as they hold no analytical value.
    cleaned_df = df.dropna(subset=['Price_KSh'])
    
    logging.info(f"Transformation successful. Records processed: {len(cleaned_df)}")
    return cleaned_df

def generate_market_report(df: pd.DataFrame):
    """
    Aggregates cleaned data to provide business insights on Subaru models.
    """
    logging.info("Calculating market averages...")
    
    # Using Pandas Vectorization for high-performance aggregation
    summary = df.groupby('Model')['Price_KSh'].mean().sort_values(ascending=False)
    
    print("\n" + "="*30)
    print("  SUBARU MARKET REPORT (KSh)")
    print("="*30)
    print(summary)
    print("="*30)

if __name__ == "__main__":
    # Mock Raw Data: Simulating the 'messy' reality of a web-scraping source
    raw_payload = {
        'Model': ['Forester', 'Impreza', 'Outback', 'Legacy', 'XV'],
        'Price_KSh': [1800000, 950000, 2200000, 'invalid_data', 2500000],
        'Year': [2018, 2015, 2019, 2017, 2021]
    }
    
    try:
        # Execute Pipeline
        df_raw = pd.DataFrame(raw_payload)
        df_clean = transform_data(df_raw)
        generate_market_report(df_clean)
        logging.info("Pipeline executed successfully.")
        
    except Exception as e:
        logging.error(f"Critical Pipeline Failure: {e}")
