Team 01 - Dashboard for the evaluation of the effect of low emission zones 

Running the app:
To run the program go to the current folder and use the command
    
    docker-compose up -d
    
Note: don't forget to first clone the repository 
    
    git clone https://github.com/R-Zaid/DSS-project
    
and go the the page in your browser
http://localhost:8080

Link to the Video: NA
Link to the Codebase: 
Dataset: 
Other Links: NA

This deliverable contains the following folders:
1. Dashboard - 
    1. pychache -
    2. preprocessors -
        1. CBSPreprocessor.ipynb -
        2. georef-netherlands-provincie.geojson -
        3. georef-netherlands-provincie.geojson -
    3. src -
        1. html -
            * dashboard.html -
            * index.html -
    


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
       * KPI: Line chart visualizes NO₂, PM₂.₅, and PM₁₀ emission trends over time to support scenario analysis.
    2. Visualization maps.jpynb: maps with LEZ locations and provinces division
       * CSF: Air pollution rates NO₂, PM₂.₅, PM₁₀, (µg/m³) per province
       * KPI: Hourly API data ensures accurate national air quality updates and displays the AQI scale in a clear, color-coded format.
    3. Visalisation NO₂ value for each province, calculated from hourly API data by mapping  provinces and average NO2 This is colored according to the European Air Quality Index (AQI) scale, from green (“Good”) to purple (“Extremely Poor”).
       * CSF: Air pollution rates NO₂, PM₂.₅, PM₁₀, (µg/m³) per province
       * KPI: Hourly API data ensures accurate national air quality updates and displays the AQI scale in a clear, color-coded format.


Data sources:
    
* georef-netherlands-provincie.geojson, georef-netherlands-provincie.geojson: 
    https://public.opendatasoft.com/explore/assets/georef-netherlands-provincie/export/
* Luchtmeetnet API  provides hourly NO₂, PM₂.₅, and PM₁₀ data. https://api-docs.luchtmeetnet.nl/
* EEA Air Quality Index –defines the AQI thresholds and color scale used in the visualization. https://airindex.eea.europa.eu/AQI/index.html
