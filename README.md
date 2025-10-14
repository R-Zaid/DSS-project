Team 01 - Dashboard for the evaluation of the effect of low emission zones 

Running the app:
To run the program go to the current folder and use the command
    
    docker-compose up -d
    
Note: don't forget to first clone the repository 
    
    'git clone https://github.com/R-Zaid/DSS-project' 
    
and go the the page in your browser
http://localhost:8080

Link to the Video: NA
Link to the Codebase: 
Dataset: 
Other Links: NA

This deliverable contains the following folders:
1. Dashboard


2. Preprocessors - Contains all the preprocessed data explaining showing how the data is collected and prepared:
    
    1.  DSS group 1 merge.jpynb - In this file we analyzed, transformed and preprocessed the api data from the following 4 APIs:
        * Vehicle api: "https://opendata.cbs.nl/ODataApi/odata/85235NED/TypedDataSet"
        * NO2 api: "https://api.luchtmeetnet.nl/open_api/measurements?formula=NO2"
        * PM2.5 api: "https://api.luchtmeetnet.nl/open_api/measurements?formula=PM25"
        * PM10 api: "https://api.luchtmeetnet.nl/open_api/measurements?formula=PM10"

        The last three APIs are frequently updated (once every hour).
    
    2. Map_No2.jpynb
    
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
    2. Visualization maps.jpynb: maps with LEZ locations and provinces division
    3. Visalisation NO₂ value for each province, calculated from hourly API data by mapping  provinces and average NO2 This is colored according to the European Air Quality Index (AQI) scale, from green (“Good”) to purple (“Extremely Poor”).
