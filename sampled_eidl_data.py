import pandas as pd
from tqdm import tqdm

# List of files to load.
files = ["EIDL/DATAACT_EIDL_LOANS_20200401-20200609.csv",
         "EIDL/DATAACT_EIDL_LOANS_20200610-20200625.csv",
         "EIDL/DATAACT_EIDL_LOANS_20200626-20200723.csv",
         "EIDL/DATAACT_EIDL_LOANS_20200724-20201115.csv",
         "EIDL/DATAACT_EIDL_LOANS_DMCS2.0.csv"
]

# Fraction of data to sample.
fraction_of_data = 0.2

# Initialize an empty DataFrame.
eidl_data = pd.DataFrame()

# Specify the columns to load.
columns_to_load = ['ACTIONDATE', 'PRIMPLACEOFPERFORMANCECD', 'FACEVALUEOFDIRECTLOANORLOANGUARANTEE']

# Loop through the files and load the data.
for file in tqdm(files):
    temp_df = pd.read_csv(file, usecols=columns_to_load)
    temp_df = temp_df.sample(frac=fraction_of_data, random_state=42)
    eidl_data = pd.concat([eidl_data, temp_df])

# Create a new variable in the EIDL data frame that takes the value “EIDL” for all rows.
eidl_data['LoanProgram'] = 'EIDL'

# Extract the State from the PRIMPLACEOFPERFORMANCECD variable.
eidl_data['State'] = eidl_data['PRIMPLACEOFPERFORMANCECD'].str[:2]

# Drop the PRIMPLACEOFPERFORMANCECD column as it's no longer needed.
eidl_data.drop(columns=['PRIMPLACEOFPERFORMANCECD'], inplace=True)

# Convert ACTIONDATE to datetime format
eidl_data['ACTIONDATE'] = pd.to_datetime(eidl_data['ACTIONDATE'], format='%Y%m%d', errors='coerce')

# Rename the columns
eidl_data.rename(columns={
    'FACEVALUEOFDIRECTLOANORLOANGUARANTEE': 'Loan',
    'ACTIONDATE': 'Date'
}, inplace=True)

# Save the cleaned DataFrame to a new CSV file
eidl_data.to_csv(f'combined_eidl_data_{fraction_of_data}.csv', index=False)

# Display the first few rows of the DataFrame.
print(eidl_data.head())
