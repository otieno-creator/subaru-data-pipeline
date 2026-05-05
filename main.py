"""
Subaru Market Data Pipeline
Author: Dan Otieno (AWS Security Champion)
Description: A production-grade ETL pipeline featuring Type Hinting, 
Defensive Programming, and Cloud-ready architecture.
"""

import pandas as pd
import logging
from typing import Dict, Any

# 1. PRODUCTION LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleanses raw marketplace data using defensive programming.
    Returns: A validated pandas DataFrame.
    """
    logging.info("Initiating Data Transformation...")

    # Defensive Casting: Type safety for price and year
    df['Price_KSh'] = pd.to_numeric(df['Price_KSh'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Data Validation: Removing unusable records
    cleaned_df = df.dropna(subset=['Price_KSh'])
    
    logging.info(f"Transformation successful. Records processed: {len(cleaned_df)}")
    return cleaned_df

def generate_market_report(df: pd.DataFrame) -> None:
    """
    Aggregates cleaned data to provide business insights.
    """
    logging.info("Calculating market averages...")
    
    summary = df.groupby('Model')['Price_KSh'].mean().sort_values(ascending=False)
    
    print("\n" + "="*30)
    print("  SUBARU MARKET REPORT (KSh)")
    print("="*30)
    print(summary)
    print("="*30)

def run_pipeline(payload: Dict[str, Any]) -> None:
    """
    Orchestrates the ETL process from ingestion to reporting.
    """
    try:
        df_raw = pd.DataFrame(payload)
        df_clean = transform_data(df_raw)
        generate_market_report(df_clean)
        logging.info("Pipeline lifecycle completed successfully.")
        
    except Exception as e:
        logging.error(f"Critical Pipeline Failure: {e}")

if __name__ == "__main__":
    # Mock Raw Data: Simulating messy marketplace input
    raw_payload = {
        'Model': ['Forester', 'Impreza', 'Outback', 'Legacy', 'XV'],
        'Price_KSh': [1800000, 950000, 2200000, 'invalid_data', 2500000],
        'Year': [2018, 2015, 2019, 2017, 2021]
    }
    
    run_pipeline(raw_payload)

