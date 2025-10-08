# %%
%pip install requests
%pip install zeep
%pip install openml

# %%
import requests
from pprint import pprint
import pandas as pd
from zeep import Client
import logging
import openml
import sqlite3
import xml.etree.ElementTree as ET


# %% [markdown]
# # API Number of motor vehicles per 1,000 inhabitants 
# 
# Below you can find the end points. We will use the TypedDataSet end point.
# ```
# {
#   "odata.metadata":"https://opendata.cbs.nl/ODataApi/OData/85235NED/$metadata","value":[
#     {
#       "name":"TableInfos","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/TableInfos"
#     },{
#       "name":"UntypedDataSet","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/UntypedDataSet"
#     },{
#       "name":"TypedDataSet","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
#     },{
#       "name":"DataProperties","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/DataProperties"
#     },{
#       "name":"CategoryGroups","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/CategoryGroups"
#     },{
#       "name":"RegioS","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/RegioS"
#     },{
#       "name":"Perioden","url":"https://opendata.cbs.nl/ODataApi/odata/85235NED/Perioden"
#     }
#   ]
# }
# ```

# %%
url = "https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
response= requests.get(url)
users= response.json()
print(users)



# %% [markdown]
# ##### In order to make the output above more readable print the following cell

# %%
# this will print the typed dataset in json format, so name value pairs
url = "https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
posts = requests.get(url).json()

pprint (posts)





# %%
# select columns by first selecting the "value" key from json format
# then specify the specific columns
dfposts = pd.DataFrame(posts["value"])[['Aanhangwagen_17',
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
            'VrachtautoExclTrekkerVoorOplegger_12']]
dfposts.head()



# %%
dfposts.info()

# %%
dfposts.describe(include="all")

# %%
dfposts.isnull().sum()

# %% [markdown]
# #### Since we want to use this data to portray the impact of cars in specific regions on the air quality, we choose to use the following attributes from this data source:
# ```
# columns_vehicledb = ['Aanhangwagen_17',
#             'Bestelauto_11',
#             'Bus_15',
#             'InBezitNatuurlijkePersonenRelatief_6',
#             'InBezitNatuurlijkePersonen_5',
#             'MotorfietsenRelatief_20',
#             'Oplegger_18',
#             'PersonenautoSRelatief_4',
#             'SpeciaalVoertuig_14',
#             'TotaalAanhangwagensEnOpleggers_16',
#             'TotaalAanhangwagensEnOpleggers_9',
#             'TotaalBedrijfsmotorvoertuigen_10',
#             'TotaalBedrijfsmotorvoertuigen_8',
#             'TotaalBedrijfsvoertuigen_7',
#             'TotaalMotorfietsen_19',
#             'TotaalMotorvoertuigen_2',
#             'TotaalPersonenautoS_3',
#             'TotaalWegvoertuigen_1',
#             'TrekkerVoorOplegger_13',
#             'VrachtautoExclTrekkerVoorOplegger_12']
# 
# ```

# %%
print(dfposts["RegioS"].nunique(), "different regions")
print(dfposts["RegioS"].unique())
print(dfposts["RegioS"].value_counts())

# %% [markdown]
# There are 17 different regios, divided in the following two categories: LD (landsdeel) and PV (provincies). We choose to primiraly focus on provinces due to data granularity. 

# %%
dfprovince = dfposts[dfposts["RegioS"].str.startswith("PV")]
print(dfprovince)

# %%
columns_vehicledb = ['Aanhangwagen_17',
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
            'VrachtautoExclTrekkerVoorOplegger_12']

pvencoding = {'PV20':'Groningen',
              'PV21':'Friesland',
              'PV22':'Drenthe',
              'PV23':'Overijssel',  
              'PV24':'Flevoland',
              'PV25':'Gelderland',
              'PV26':'Utrecht',
              'PV27':'Noord-Holland',
              'PV28':'Zuid-Holland',
              'PV29':'Zeeland',
              'PV30':'Noord=Brabant',
              'PV31':'Limburg'}


dfprovince = dfprovince.groupby('RegioS')[columns_vehicledb].sum().reset_index()
dfprovince["Sum"] = dfprovince[columns_vehicledb].sum(axis=1)
dfprovince['RegioS'] = dfprovince['RegioS'].astype(str).str.strip()
dfprovince['RegioS'] = dfprovince['RegioS'].map(pvencoding)
print(dfprovince[["RegioS","Sum"]])


# %%
dftotal = dfprovince.groupby('RegioS')[columns_vehicledb].sum().sum()

dftotal["Sum"] = dftotal[columns_vehicledb].sum()

print(dftotal)

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(4,6))
sum = dfprovince['Sum'].dropna() # If you don't remove NANs, default matplotlib function will fail
plt.boxplot(sum, vert=True, patch_artist=True)
plt.title("Sum Distribution")
plt.ylabel("Sum")
plt.show()

# %%
import plotly.express as px


bar = px.bar(dfprovince, x='RegioS', y= 'Sum', title='Bar chart of sum of cars per region')
bar.update_layout(yaxis_title='Sum of cars', xaxis_title= "Region Code", barmode='group') 

bar.show()

# %% [markdown]
# ##### Standardize numerical data below, so that this data could be used for the predictive part (machine learning algorithms, such as SVM, dbscan, etc.)

# %%
from sklearn.preprocessing import StandardScaler

standardization = dfprovince[['Aanhangwagen_17',
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
            'VrachtautoExclTrekkerVoorOplegger_12']]


standardize = StandardScaler().fit_transform(standardization)

dfstandardization = pd.DataFrame(standardize, columns=standardization.columns)
print(dfstandardization)

# %%


# %% [markdown]
# #### IMPORTANT: CHOOSE SAMPLING DURING THE PREDICTIVE PART. IT IS NOW NOT POSSIBLE TO CHOOSE THIS, BECAUSE THE SAMPLES NEEDS TO BE ALIGNED WITH PM2.5 PM10 AND NO2 DATA.

# %% [markdown]
# # API Luchtmeetnet
# 
# In this part of the code, we will retrieve data from the luchtmeetnet api. We filter through the measurements using ?formula=NO2 , ?formula=PM10 and ?formula=PM25  

# %%
url = "https://api.luchtmeetnet.nl/open_api/measurements?formula=NO2" # get data from luchtmeetnet api and filter it so that only NO2 formulas will be retrieved
posts_luchtmeetnet_NO2 = requests.get(url).json()
#pprint(posts_luchtmeetnet_NO2)



# %%
url = "https://api.luchtmeetnet.nl/open_api/measurements?formula=PM25" # get data from luchtmeetnet api and filter it so that only PM25 formulas will be retrieved
posts_luchtmeetnet_PM25 = requests.get(url).json()
#pprint(posts_luchtmeetnet_PM25)


# %%
url = "https://api.luchtmeetnet.nl/open_api/measurements?formula=PM10" # get data from luchtmeetnet api and filter it so that only PM10 formulas will be retrieved
posts_luchtmeetnet_PM10 = requests.get(url).json()
#pprint(posts_luchtmeetnet_PM10)

# %% [markdown]
# We know want to put it in a dataframe 

# %%
dfposts_NO2 = pd.DataFrame(posts_luchtmeetnet_NO2["data"])[['formula',
           'station_number',
           'timestamp_measured',
           'value']]
dfposts_NO2.head(10)

# %%
dfposts_PM25 = pd.DataFrame(posts_luchtmeetnet_PM25["data"])[['formula',
           'station_number',
           'timestamp_measured',
           'value']]
dfposts_PM25.head(10)

# %%
dfposts_PM10 = pd.DataFrame(posts_luchtmeetnet_PM10["data"])[['formula',
           'station_number',
           'timestamp_measured',
           'value']]
dfposts_PM10.head(10)

# %% [markdown]
# # API Population density
# 
# ```
# {
#   "odata.metadata":"https://opendata.cbs.nl/ODataApi/OData/85984NED/$metadata","value":[
#     {
#       "name":"TableInfos","url":"https://opendata.cbs.nl/ODataApi/odata/85984NED/TableInfos"
#     },{
#       "name":"UntypedDataSet","url":"https://opendata.cbs.nl/ODataApi/odata/85984NED/UntypedDataSet"
#     },{
#       "name":"TypedDataSet","url":"https://opendata.cbs.nl/ODataApi/odata/85984NED/TypedDataSet"
#     },{
#       "name":"DataProperties","url":"https://opendata.cbs.nl/ODataApi/odata/85984NED/DataProperties"
#     },{
#       "name":"CategoryGroups","url":"https://opendata.cbs.nl/ODataApi/odata/85984NED/CategoryGroups"
#     },{
#       "name":"WijkenEnBuurten","url":"https://opendata.cbs.nl/ODataApi/odata/85984NED/WijkenEnBuurten"
#     }
#   ]
# }
# ```
# 
# * https://learn.microsoft.com/en-us/odata/concepts/queryoptions-overview -> explains how to use batches since thi API needs to parse from a very large data source. Since it is a very large data set, we will print the first 9000 rows before we begin with preprocessing

# %% [markdown]
# ### NOTE: it is still not on the same abstraction level as the other APIs. To fix this, we need to specify codering_3 to only values that start with NL

# %%
url_population = "https://opendata.cbs.nl/ODataApi/odata/85984NED/TypedDataSet?$top=9000&$skip=0"
response_population= requests.get(url_population)
users_population= response.json()
posts_population = requests.get(url_population).json()

#pprint (posts_population)

# %%
dfposts_population = pd.DataFrame(posts_population["value"])[['Bevolkingsdichtheid_34',
           'Codering_3',
           'Gemeentenaam_1']]
dfposts_population.head(10)

# %% [markdown]
# ## Note: DISCUSS IF IT IS USEFUL TO EVEN USE THIS SPECIFIC DATASET SINCE IT IS DIFFICULT TO EASILY LINK IT TO THE REGIOS ID OF THE API DATASET

# %%
dffiltered = dfposts_population[dfposts_population["Codering_3"].str.startswith("GM")]


dffiltered.value_counts() #154 Gemeentes
dfposts_population.value_counts() # Codering_3 has a total of lenght of 8527

# %% [markdown]
# # XML emission zone

# %%
!pip install xmltodict

# %%
!pip install lxml

# %% [markdown]
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <mc:messageContainer xmlns:mc="http://datex2.eu/schema/3/messageContainer" xmlns:nlxe="http://datex2.eu/schema/3/nlxExtensions" xmlns:inf="http://datex2.eu/schema/3/informationManagement" xmlns:comx="http://datex2.eu/schema/3/commonExtension" xmlns:cz="http://datex2.eu/schema/3/controlledZone" xmlns:ex="http://datex2.eu/schema/3/exchangeInformation" xmlns:tro="http://datex2.eu/schema/3/trafficRegulation" xmlns:loc="http://datex2.eu/schema/3/locationReferencing" xmlns:com="http://datex2.eu/schema/3/common" modelBaseVersion="3"><mc:payload xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

# %%


import xml.etree.cElementTree as ET
tree = ET.parse(r'C:\Users\Ratiba Zaid\Downloads\emissiezones.xml\emissiezones.xml')
root = tree.getroot()

print(root.tag)
print(root.attrib)

print(root)
#namespace from julian's code
name_space = {
    'mc': 'http://datex2.eu/schema/3/messageContainer',
    'ex': 'http://datex2.eu/schema/3/exchange',
    'com': 'http://datex2.eu/schema/3/common',
    'comx': 'http://datex2.eu/schema/3/commonExtension',
    'cz': 'http://datex2.eu/schema/3/controlledZone',
    'tro': 'http://datex2.eu/schema/3/trafficRegulationOrder',
    'loc': 'http://datex2.eu/schema/3/locationReferencing',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

for elements in root.findall(".//loc:locationReferencing", name_space):
    print(elements.tag, elements.attrib)


# %% [markdown]
# ##### JULIAN's code from untitled.ipynb=> first cell

# %%
# Read the XML file
xml_file_path = r'C:\Users\Ratiba Zaid\Downloads\emissiezones.xml\emissiezones.xml'

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

print(f"Root element: {root.tag}")
print(f"Root attributes: {root.attrib}")

# Find all emission zones
emission_zones = []

# Define correct namespaces based on the actual XML structure
namespaces = {
    'mc': 'http://datex2.eu/schema/3/messageContainer',
    'ex': 'http://datex2.eu/schema/3/exchange',
    'com': 'http://datex2.eu/schema/3/common',
    'comx': 'http://datex2.eu/schema/3/commonExtension',
    'cz': 'http://datex2.eu/schema/3/controlledZone',
    'tro': 'http://datex2.eu/schema/3/trafficRegulationOrder',
    'loc': 'http://datex2.eu/schema/3/locationReferencing',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Find controlled zone table
controlled_zone_table = root.find('.//cz:controlledZoneTable', namespaces)
if controlled_zone_table is not None:
    # Find all urban vehicle access regulations
    access_regulations = controlled_zone_table.findall('.//cz:urbanVehicleAccessRegulation', namespaces)
    
    print(f"\nFound {len(access_regulations)} emission zones")
    
    for regulation in access_regulations:
        zone_data = {}
        
        # Extract zone name
        name_element = regulation.find('.//cz:name/com:values/com:value[@lang="nl"]', namespaces)
        zone_data['name'] = name_element.text if name_element is not None else "Unknown"
        
        # Extract zone type
        zone_type_element = regulation.find('.//cz:controlledZoneType', namespaces)
        zone_data['type'] = zone_type_element.text if zone_type_element is not None else "Unknown"
        
        # Extract URL for further information
        url_element = regulation.find('.//cz:urlForFurtherInformation', namespaces)
        zone_data['url'] = url_element.text if url_element is not None else ""
        
        # Extract status
        status_element = regulation.find('.//cz:status', namespaces)
        zone_data['status'] = status_element.text if status_element is not None else "Unknown"
        
        # Extract issuing authority
        authority_element = regulation.find('.//tro:issuingAuthority/com:values/com:value[@lang="nl"]', namespaces)
        zone_data['authority'] = authority_element.text if authority_element is not None else "Unknown"
        
        # Extract regulation ID
        regulation_id_element = regulation.find('.//tro:regulationId', namespaces)
        zone_data['regulation_id'] = regulation_id_element.text if regulation_id_element is not None else "Unknown"
        
        # Extract validity period
        start_time_element = regulation.find('.//com:overallStartTime', namespaces)
        end_time_element = regulation.find('.//com:overallEndTime', namespaces)
        zone_data['start_date'] = start_time_element.text if start_time_element is not None else "Unknown"
        zone_data['end_date'] = end_time_element.text if end_time_element is not None else "Unknown"
        
        # Extract location coordinates (simplified - just count)
        coordinates = regulation.findall('.//loc:posList', namespaces)
        zone_data['coordinate_sets'] = len(coordinates)
        
        # Extract vehicle restrictions
        vehicle_conditions = regulation.findall('.//tro:vehicleCharacteristics', namespaces)
        zone_data['vehicle_restrictions'] = len(vehicle_conditions)
        
        emission_zones.append(zone_data)

print(emission_zones)

# %%



