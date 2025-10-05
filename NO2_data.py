#import os
#import pandas as pd
#pad = r'C:\Users\enock\Python projects\2016_NO2.csv' 
#df = pd.read_csv(pad,skiprows=5,nrows=15,sep=';')

#main_df=pd.DataFrame()
#gemiddelden_per_bestand = {}
#for x in os.listdir(r'C:\Users\enock\Python projects'):
    #if x.endswith('NO2.csv'):
        #file_path = os.path.join(r'C:\Users\enock\Python projects', x)
        #temp_df = pd.read_csv(file_path, skiprows=5, sep=';')
        #gemiddelde = temp_df['waarde'].mean()
        #gemiddelden_per_bestand[x] = gemiddelde
        #main_df = pd.concat([main_df, temp_df], ignore_index=True)
#main_df.drop(columns=['opm_code'], inplace=True)

#resultaten_df = pd.DataFrame(
    #list(gemiddelden_per_bestand.items()), 
    #columns=['Bestand', 'Gemiddelde NO2 Waarde']
#)

#print(resultaten_df)
import pandas as pd

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
main_df = pd.DataFrame()
gemiddelden_per_bestand = {}


for base_url in urls:
    
    year = base_url.split('/')[-2]
    
    file_name = year + csv_suffix
    full_url = base_url + file_name 
    
    print("Bezig met verwerken: {}".format(file_name)) 


    temp_df = pd.read_csv(full_url, index_col = 0, skiprows=5, sep=';')
    
    gemiddelde = temp_df['waarde'].mean()
    gemiddelden_per_bestand[file_name] = gemiddelde
    
    main_df = pd.concat([main_df, temp_df], ignore_index=True)
    
if 'opm_code' in main_df.columns:
    main_df.drop(columns=['opm_code'], inplace=True)

resultaten_df = pd.DataFrame( list(gemiddelden_per_bestand.items()),
columns=['Bestand (Jaar)', 'Gemiddelde NO2 Waarde']
)

resultaten_df["Jaar"] = resultaten_df["Bestand (Jaar)"].str.split('_').str[0]

resultaten_df = resultaten_df.drop(columns=["Bestand (Jaar)"])

resultaten_df = resultaten_df[['Jaar', 'Gemiddelde NO2 Waarde']]

print(resultaten_df)