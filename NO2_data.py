import pandas as pd
import numpy as np

urls = [
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/1990/', 
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2016/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2017/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2018/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2019/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2020/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2021/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2022/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2023/',
    'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2024/',
]
csv_suffix = '_NO2.csv' 
all_dfs = [] 


for base_url in urls:
    
    year = base_url.split('/')[-2]
    file_name = year + csv_suffix
    full_url = base_url + file_name 
    
   
    temp_df = pd.read_csv(
        full_url, 
        sep=';', 
        skiprows=5 
    )
    
    all_dfs.append(temp_df)
    print(f"loaded: {file_name}")

#Combine data into one df
main_df = pd.concat(all_dfs, ignore_index=True)

# convert date to  datetime
main_df['begindatumtijd'] = pd.to_datetime(main_df['begindatumtijd'], errors='coerce')

# Make a new column for Year-Month 
main_df['Jaar_Maand'] = main_df['begindatumtijd'].dt.to_period('M')

# Group by the new Year_Month column and calculate the mean of 'waarde'
monthlyaverage_df = main_df.groupby('Jaar_Maand')['waarde'].mean().reset_index()

# Rename the columns
monthlyaverage_df.columns = ['Year_Month', 'Average NO2 Value']

# Format year and month column for better display
monthlyaverage_df['Year_Month'] = monthlyaverage_df['Year_Month'].astype(str)
monthlyaverage_df['Average NO2 Value'] = monthlyaverage_df['Average NO2 Value'].round(0).astype(int)


print(monthlyaverage_df)
output_filename = 'mean_no2_monthlyvalues.csv'
monthlyaverage_df.to_csv(output_filename, index=False, sep=',')
