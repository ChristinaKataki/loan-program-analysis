import pandas as pd
from tqdm import tqdm

# List of files to load
files = ["RawData/public_150k_plus_230930.csv"] + [f'RawData/public_up_to_150k_{i}_230930.csv' for i in range(1, 13)]

# Fraction of data to sample
fraction_of_data = 0.1

# Initialize an empty DataFrame
df = pd.DataFrame()

# Specify the columns to load
columns_to_load = ['CurrentApprovalAmount', 'BorrowerState', 'DateApproved', 'NAICSCode']

# Loop through the files and load the data
for file in tqdm(files):
    temp_df = pd.read_csv(file, usecols=columns_to_load)
    temp_df = temp_df.sample(frac=fraction_of_data, random_state=42)
    df = pd.concat([df, temp_df])

# Keep the first two digits from the NAICS Code
df['NAICSCode'] = df['NAICSCode'].astype(str).str[:2]

# Add the LoanProgram variable
df['LoanProgram'] = 'PPP'

# Convert DateApproved to datetime format
df['DateApproved'] = pd.to_datetime(df['DateApproved'], format='%m/%d/%Y', errors='coerce')

# Rename the columns
df.rename(columns={
    'CurrentApprovalAmount': 'Loan',
    'BorrowerState': 'State',
    'DateApproved': 'Date',
    'NAICSCode': 'NAICS'
}, inplace=True)

# Save the combined DataFrame to a new CSV file.
df.to_csv(f"CovidRecovery/final_combined_ppp_{fraction_of_data}.csv", index=False)

# Display the first few rows of the DataFrame.
print(df.head())
