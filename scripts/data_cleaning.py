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


# new customers with missing TotalCharges will have a tenure of 0, so we can fill those with 0
# Fill with MonthlyCharges (since TotalCharges = MonthlyCharges * tenure for new customers)
df.loc[missing_total, 'TotalCharges'] = df.loc[missing_total, 'MonthlyCharges']

print(f"Filled {missing_total.sum()} missing TotalCharges with MonthlyCharges for new customers")

# Standardize yes/no columns to 1/0
df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
print(f"Converted SeniorCitizen to Yes/No depending on value")

# creating derived features for analysis
print("\n Creating derived features...")

# Tenure groups - categorizing customers based on their tenure with the company
df['TenureGroup'] = pd.cut(df['tenure'],
                     bins=[0, 12, 24, 48, 72],
                     labels=['0-1 year', '1-2 years', '2-4 years', '4+ years'])
# what the code above does is it creates a new column called TenureGroup which categorizes customers based on their tenure with the company.
# meaning, if a customer has a tenure of 0-12 months, categorized as 0-1 year, 13-24 months as 1-2 years and so on.
# this will help us analyze the churn rates based on how long customers have been with the company.

# Monthly charges groups - categorizing customers based on their monthly charges
df['ChargeLevel'] = pd.cut(df['MonthlyCharges'],
                             bins=[0, 30, 60, 90, 150],
                             labels=['Low ($0-30)', 'Medium ($30-60)', 'High ($60-90)', 'Very High ($90+)'])

# total add-on services
service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

# Count Yes across service columns 
df['TotalServices'] = 0
for col in service_cols:
    df['TotalServices'] = df['TotalServices'] + (df[col] == 'Yes').astype(int)

# Customer lifetime value 
df['EstimatedCLV'] = df['MonthlyCharges'] * df['tenure']
print(" Created TenureGroup, ChargeLevel, TotalServices, and EstimatedCLV features")


# binary churn flag, now we binary col for churn, yes=1 no=0
# now we will convert the churn col to a binary col where yes=1 and no=0
mapping = {'Yes': 1, 'No': 0}
df['ChurnFlag'] = df['Churn'].map(mapping)
print(" Created binary ChurnFlag col where yes=1 and no=0")

# remove any existing duplicates if there is any

