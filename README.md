Team 01 - Dashboard for the evaluation of the effect of low emission zones 

For the Deployment of our program we run a docker compose file that consists of three endpoints. - -The first endpoint is a postgres database hosted on 5432, set up just like the one in the example code snippit. The second endpoint is our old code from the midterm report, it uses flask to run an html folder structure. This endpoint is outdated and should not be considered in the final exam. However, we chose not to delete it as it is a nice way of showing the difference between the midterm and the final product. The last endpoint is our final product, the streamlit-app. It is hosted on port: 8501, which is a standard streamlit endpoint.  

 

By having docker open and running the command: docker-compose up –d streamlit-app, you start our application and can begin to see the projectIf this does not work immidiately you can change  

db_dashboard-data:/var/lib/postgresql 

Into 

 db_dashboard-data:/var/lib/postgresql/data/ 

 If the map is empty run this command: docker-compose exec streamlit-app python /app/load_yearly_averages.py. 
 This fills the database. However it should already be working. This is just a failsave. 

 
    
Note: don't forget to first clone the repository 
    
    git clone https://github.com/R-Zaid/DSS-project
    
and go the the page in your browser
http://localhost:8501

Link to the Video: NA
Link to the Codebase: 
Dataset: 
Other Links: NA

This deliverable contains the following folders:
1. Dashboard - 
    dashboard.py - our streamlit app that runs everything. And is the only actual important file in the dashboard part except for the data. 
    4. dockerfile_dashboard - contains the docker for the dashboard. Looks a lot like the one from the example code.
    5. Requirements.txt - a lot of standard data frameworks. We have already imported streamlit as we want to use this in the future for clean UI design. We use earthpy, geopandas, folium and dash for creation of better diagrams. The version specification is needed as otherwise it creates an error. 


2. Preprocessors - Contains all the preprocessed data explaining and showing how the data is collected and prepared:
    
    1.  DSS group 1 merge.jpynb - In this file we analyzed, transformed and preprocessed the api data from the following 4 APIs:
        * Vehicle api: "https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
        * NO2 api: "https://api.luchtmeetnet.nl/open_api/measurements?formula=NO2"
        * PM2.5 api: "https://api.luchtmeetnet.nl/open_api/measurements?formula=PM25"
        * PM10 api: "https://api.luchtmeetnet.nl/open_api/measurements?formula=PM10"

        The last three APIs are frequently updated (once every hour). This file comprehensively explained how we preprocessed each api. For the pollution api we cleaned and transformed the datasets. Subsequently, we made visualizations where we visualized each stations and regions alongside their measured pollution value. Also, this file contains visualizations which are created to help us understand the dataset. Furthermore, each part of the file contains an explanation regarding our preprocess approaches. 
    
    2. Map_No2.jpynb - This file focuses on creating the map of the netherlands for the first deliverable. However it still needs to be merged with the DSS group 1 merge.ipnby (adddd)
    
    3. NO2_dataset.jpynb - Adds the monthly mean value for the descriptive part of the dashboard. This file will also be used to predict the NO2 values.
       * Data Sources: RIVM luchtmeetnet  
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/1990/', 
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2016/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2017/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2018/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2019/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2020/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2021/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2022/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2023/',
            'https://data.rivm.nl/data/luchtmeetnet/Vastgesteld-jaar/2024/'


3. Existing Indicators and Visualizations:
    1. Vis NO2.jpynb: visualization of historical values of NO2 form 2016 to 2024
       * CSF: Predict emissions per region in 2030 scenarios of low emission zones
       * KPI: Line chart visualizes NO2, PM₂.₅, and PM₁₀ emission trends over time to support scenario analysis.
    2. Visualization maps.jpynb: maps with LEZ locations and provinces division
       * CSF: Air pollution rates NO2, PM₂.₅, PM₁₀, (µg/m³) per province
       * KPI: Hourly API data ensures accurate national air quality updates and displays the AQI scale in a clear, color-coded format.
    3. Visalisation NO2 value for each province, calculated from hourly API data by mapping  provinces and average NO2 This is colored according to the European Air Quality Index (AQI) scale, from green (“Good”) to purple (“Extremely Poor”).
       * CSF: Air pollution rates NO2, PM₂.₅, PM₁₀, (µg/m³) per province
       * KPI: Hourly API data ensures accurate national air quality updates and displays the AQI scale in a clear, color-coded format.


Data sources:
    
* georef-netherlands-provincie.geojson, georef-netherlands-provincie.geojson: 
    https://public.opendatasoft.com/explore/assets/georef-netherlands-provincie/export/
* Luchtmeetnet API  provides hourly NO2, PM₂.₅, and PM₁₀ data. https://api-docs.luchtmeetnet.nl/
* EEA Air Quality Index –defines the AQI thresholds and color scale used in the visualization. https://airindex.eea.europa.eu/AQI/index.html
