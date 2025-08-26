#!/usr/bin/env python3
"""
Fix CSV data to ensure proper column separation
"""

import pandas as pd
import os

# Read the existing CSV file
df = pd.read_csv('ceo_sourcing_results.csv')

# Create new columns for company description
df['Company Description'] = ''  # Empty for now, will be populated by the updated script
df['Description Confidence'] = ''
df['Description Sources'] = ''

# Remove the old CEO background columns
columns_to_drop = ['CEO Background', 'Background Confidence', 'Background Sources']
df = df.drop(columns=columns_to_drop, errors='ignore')

# Reorder columns to match the new structure
column_order = [
    'Company', 'Website', 'CEO', 'CEO Confidence', 'CEO Sources',
    'CEO LinkedIn', 'LinkedIn Confidence', 'LinkedIn Sources',
    'Company Description', 'Description Confidence', 'Description Sources',
    'Market Research', 'Market Confidence', 'Market Sources',
    'Parallel Use Case', 'UseCase Confidence', 'UseCase Sources'
]

# Reorder columns (only include columns that exist)
existing_columns = [col for col in column_order if col in df.columns]
df = df[existing_columns]

# Save the updated CSV
df.to_csv('ceo_sourcing_results.csv', index=False)

print("✅ CSV file updated successfully!")
print("✅ Removed CEO background columns")
print("✅ Added company description columns")
print(f"✅ Final columns: {list(df.columns)}")


