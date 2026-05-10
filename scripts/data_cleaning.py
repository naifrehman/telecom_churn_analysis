import numpy as np
import pandas as pd

print("This script is used to clean the data for the project, containing the data cleaning pipeline.")

# load the raw data csv file 
df = pd.read_csv('C:\\Users\\nayef\\OneDrive\\Desktop\\telecom-churn-analysis\\data\\raw\\telco_churn.csv')
print(f"Loaded: {len(df)} rows and {len(df.columns)} columns")


# will convert the total charges column to numeric, and if not numeric, will set to NaN using error='coerce' which will replace non-numeric values with NaN
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

print('Fixing TotalCharges Column...')
# convert to numeric, or set to NaN if not numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
missing_total = df['TotalCharges'].isna()
print(f"Found {missing_total.sum()} rows with missing TotalCharges")
