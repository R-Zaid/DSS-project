#libs 
import requests
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
from flask import Flask, jsonify

# this will print the typed dataset in json format, so name value pairs
url = "https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
response = requests.get(url)
users = response.json()
#print(users)

url = "https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
posts = requests.get(url).json()
pprint(posts)

# select columns by first selecting the "value" key from json format
# then specify the specific columns
dfposts = pd.DataFrame(posts["value"])[[
    'Aanhangwagen_17',
    'Bestelauto_11',
    'Bus_15',
    'ID',
    'InBezitNatuurlijkePersonenRelatief_6',
    'InBezitNatuurlijkePersonen_5',
    'MotorfietsenRelatief_20',
    'Oplegger_18',
    'Perioden',
    'PersonenautoSRelatief_4',
    'RegioS',
    'SpeciaalVoertuig_14',
    'TotaalAanhangwagensEnOpleggers_16',
    'TotaalAanhangwagensEnOpleggers_9',
    'TotaalBedrijfsmotorvoertuigen_10',
    'TotaalBedrijfsmotorvoertuigen_8',
    'TotaalBedrijfsvoertuigen_7',
    'TotaalMotorfietsen_19',
    'TotaalMotorvoertuigen_2',
    'TotaalPersonenautoS_3',
    'TotaalWegvoertuigen_1',
    'TrekkerVoorOplegger_13',
    'VrachtautoExclTrekkerVoorOplegger_12'
]]

dfposts.head()

dfposts.info()

dfposts.describe(include="all")

dfposts.isnull().sum()

#print(dfposts["RegioS"].nunique(), "different regions")
#print(dfposts["RegioS"].unique())
#print(dfposts["RegioS"].value_counts())

dfprovince = dfposts[dfposts["RegioS"].str.startswith("PV")]
#print(dfprovince)

columns_vehicledb = [
    'Aanhangwagen_17',
    'Bestelauto_11',
    'Bus_15',
    'InBezitNatuurlijkePersonenRelatief_6',
    'InBezitNatuurlijkePersonen_5',
    'MotorfietsenRelatief_20',
    'Oplegger_18',
    'PersonenautoSRelatief_4',
    'SpeciaalVoertuig_14',
    'TotaalAanhangwagensEnOpleggers_16',
    'TotaalAanhangwagensEnOpleggers_9',
    'TotaalBedrijfsmotorvoertuigen_10',
    'TotaalBedrijfsmotorvoertuigen_8',
    'TotaalBedrijfsvoertuigen_7',
    'TotaalMotorfietsen_19',
    'TotaalMotorvoertuigen_2',
    'TotaalPersonenautoS_3',
    'TotaalWegvoertuigen_1',
    'TrekkerVoorOplegger_13',
    'VrachtautoExclTrekkerVoorOplegger_12'
]

# province names to dict key's -> easier access 
pvencoding = {
    'PV20': 'Groningen',
    'PV21': 'Friesland',
    'PV22': 'Drenthe',
    'PV23': 'Overijssel',
    'PV24': 'Flevoland',
    'PV25': 'Gelderland',
    'PV26': 'Utrecht',
    'PV27': 'Noord-Holland',
    'PV28': 'Zuid-Holland',
    'PV29': 'Zeeland',
    'PV30': 'Noord=Brabant',
    'PV31': 'Limburg'
}

dfprovince = dfprovince.groupby('RegioS')[columns_vehicledb].sum().reset_index()
dfprovince["Sum"] = dfprovince[columns_vehicledb].sum(axis=1)
dfprovince['RegioS'] = dfprovince['RegioS'].astype(str).str.strip()
dfprovince['RegioS'] = dfprovince['RegioS'].map(pvencoding)
print(dfprovince[["RegioS", "Sum"]])

dftotal = dfprovince.groupby('RegioS')[columns_vehicledb].sum().sum()


# boxplot visualisation distrivution vehicles 
plt.figure(figsize=(4, 6))
sum_values = dfprovince['Sum'].dropna()
plt.boxplot(sum_values, vert=True, patch_artist=True)
plt.title("Sum Distribution")
plt.ylabel("Sum")
plt.show()


# bar chart sum of cars per region 
dftotal_sum = dfprovince[columns_vehicledb].sum()
print(dftotal_sum)

