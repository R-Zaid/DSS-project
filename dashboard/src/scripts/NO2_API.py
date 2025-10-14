import numpy as np
import pandas as pd
import requests
import plotly.express as px


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Everything is done at runtime, we should preprocess !!!!!!!!!!!!!!!!!

url_province = "https://api.luchtmeetnet.nl/open_api/stations"

pv = ['Groningen', 'Friesland', 'Drenthe', 'Overijssel', 'Gelderland', 'Flevoland',
      'Utrecht', 'Noord-Holland', 'Zuid-Holland', 'Noord-Brabant', 'Limburg', 'Zeeland' ]

# =======================================================================================
# ---------------------------------------------------------------------------------------
# -------------------------- Get data from Luchtmeetnet API -----------------------------
# ---------------------------------------------------------------------------------------
# =======================================================================================


# Return all data from the Luchtmeetnet API
def luchtmeetnet_api_fetch():
    posts_luchtmeetnet_province = requests.get(url_province).json()
    dfposts_NO2_province = pd.DataFrame(posts_luchtmeetnet_province["data"])[['location','number']]
    return dfposts_NO2_province

# Return a specific data type from the Luchtmeetnet API
def luchtmeetnet_api_fetch_data(data):
    if(data not in ['NO2', 'PM10', 'PM2.5']):
        raise ValueError("Invalid data type. Choose from 'NO2', 'PM10', or 'PM2.5'.")
    
    # Build the URL for measurements data
    url_measurements = f"https://api.luchtmeetnet.nl/open_api/measurements?formula={data}"
    posts_luchtmeetnet_NO2 = requests.get(url_measurements).json()
    
    dfposts_NO2 = pd.DataFrame(posts_luchtmeetnet_NO2["data"])[['formula',
           'station_number',
           'timestamp_measured',
           'value']]
           
    return dfposts_NO2


# =======================================================================================
# ---------------------------------------------------------------------------------------
# -------------------------- Average NO2 per station ------------------------------------
# ---------------------------------------------------------------------------------------
# =======================================================================================

# Clean the data for NO2
def clean_NO2_data(dfposts_NO2_clean):
    
    dfposts_NO2_clean['value']= dfposts_NO2_clean['value'].mask(dfposts_NO2_clean['value'] < 0, np.nan)
    meanlocation_clean = dfposts_NO2_clean.groupby('station_number')['value'].mean().reset_index()
    
    return meanlocation_clean

def create_NO2_chart(data):
    bar_NO2_clean = px.bar(data, x='station_number' , y= 'value', title='Average µg/m³ NO2 per station')
    bar_NO2_clean.update_layout(yaxis_title='NO2 in µg/m³', xaxis_title= "Station numbers", barmode='group') 
    #bar.add_shape(type='line', y0=40, y1=40, xref='paper', x0=0, x1=1, line_color='red')
    # add a horizontal threshold line inside the plot area
    bar_NO2_clean.add_shape(
        type="line",
        xref="paper",
        x0=0,
        x1=1,
        y0=40,
        y1=40,
        line=dict(dash="5px", color='red'),
    )

    # place a label for the line inside the plot (not in the legend)
    bar_NO2_clean.add_annotation(
        xref='paper',
        x=0.99,
        y=40,
        yref='y',
        text='Threshold 40 µg/m³',
        showarrow=False,
        xanchor='right',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='rgba(0,0,0,0.1)',
    )
    return bar_NO2_clean.to_html(full_html=False)


# Function to fetch, clean, and create the NO2 chart
def draw_NO2_chart():
    dfposts_NO2 = luchtmeetnet_api_fetch_data('NO2')
    meanlocation_clean = clean_NO2_data(dfposts_NO2)
    bar_NO2_clean_html = create_NO2_chart(meanlocation_clean)
    print("NO2 chart created")
    return bar_NO2_clean_html

# =======================================================================================
# ---------------------------------------------------------------------------------------
# -------------------------- Average NO2 per province -----------------------------------
# ---------------------------------------------------------------------------------------
# =======================================================================================

NO2_pvencoding={'NL49703': 'Noord-Holland',
                  'NL49553': 'Noord-Holland',
                  'NL01493': 'Zuid-Holland',
                  'NL10404': 'Zuid-Holland',
                  'NL10318': 'Zeeland',
                  'NL01912': 'Zeeland',
                  'NL10742': 'Groningen',
                  'NL10538': 'Noord-Holland',
                  'NL01496': 'Zuid-Holland',
                  'NL01495': 'Zuid-Holland', 
                  'NL49007': 'Noord-Holland',
                  'NL10636': 'Utrecht',
                  'NL49564': 'Noord-Holland',
                  'NL10818': 'Overijssel',
                  'NL10550': 'Noord-Holland',
                  'NL49546': 'Noord-Holland',
                  'NL10136': 'Limburg',
                  'NL10235': 'Noord-Brabant',
                  'NL01913': 'Zeeland',
                  'NL10918': 'Friesland',
                  'NL01487': 'Zuid-Holland',
                  'NL10639': 'Utrecht',
                  'NL01497': 'Zeeland',
                  'NL10644': 'Utrecht',
                  'NL10633': 'Utrecht',
                  'NL10741': 'Gelderland',
                  'NL10437': 'Zeeland',
                  'NL10247':'Noord-Brabant', 
                  'NL10445':'Zeeland',
                  'NL10934': 'Friesland',
                  'NL01494': 'Zuid-Holland',
                  'NL10449': 'Zuid-Holland',
                  'NL49017': 'Noord-Holland',
                  'NL49551': 'Noord-Holland',
                  'NL10617': 'Flevoland', 
                  'NL10442': 'Zuid-Holland',
                  'NL10446': 'Zuid-Holland',
                  'NL49565': 'Noord-Holland',
                  'NL10418':'Zuid-Holland',
                  'NL10138': 'Limburg',
                  'NL10450': 'Zuid-Holland',
                  'NL10929': 'Drenthe',
                  'NL49561': 'Noord-Holland', 
                  'NL01485': 'Zuid-Holland',
                  'NL49003': 'Noord-Holland',
                  'NL10246': 'Noord-Brabant', 
                  'NL10133': 'Limburg',
                  'NL49020': 'Noord-Holland', 
                  'NL10444': 'Zuid-Holland',  
                  'NL10738': 'Gelderland',
                  'NL10107': 'Groningen',
                  'NL49680': 'Flevoland', 
                  'NL10643': 'Zuid-Holland', 
                  'NL10248': 'Noord-Brabant', 
                  'NL10240': 'Noord-Holland', 
                  'NL10230': 'Noord-Brabant',
                  'NL10131': 'Limburg', 
                  'NL49021': 'Noord-Holland',
                  'NL10938': 'Zuid-Holland',
                  'NL49019': 'Noord-Holland',
                  'NL49014': 'Noord-Holland',
                  'NL10641': 'Utrecht', 
                  'NL01491': 'Zuid-Holland',
                  'NL10236': 'Noord-Brabant',
                  'NL10241': 'Noord-Brabant',
                  'NL49701': 'Noord-Holland',
                  'NL49012': 'Noord-Holland', 
                  'NL10722': 'Gelderland',
                  'NL49704':'Noord-Holland',
                  'NL10807': 'Overijssel',
                  'NL01488': 'Zuid-Holland', 
                  'NL10301': 'Groningen',
                  'NL10937': 'Groningen',
                  'NL49002': 'Noord-Holland',
                  'NL50010': 'Limburg',
                  'NL50002': 'Limburg', 
                  'NL50003': 'Limburg',
                  'NL54004':'Gelderland',
                  'NL01489': 'Zuid-Holland',
                  'NL49022': 'Noord-Holland',
                  'NL10237': 'Noord-Brabant'}

def transform_NO2_province(data):
    data['RegioS']  = data['station_number'].map(NO2_pvencoding)
    meanprovince = data.groupby('RegioS')['value'].mean().reset_index()
    return meanprovince

def clean_NO2_province(data):
    data['value']= data['value'].mask(data['value'] < 0, np.nan)
    return data

def create_NO2_province_chart(data):
    pv_mean = data[data['RegioS'].isin(pv)]
    bar = px.bar(pv_mean, x='RegioS' , y='value', title='Average µg/m³ NO2 per Region')
    bar.update_layout(yaxis_title='NO2 in µg/m³', xaxis_title= "Provinces", barmode='group') 
    #bar.add_shape(type='line', y0=40, y1=40, xref='paper', x0=0, x1=1, line_color='red')
    # add a horizontal threshold line inside the plot area
    bar.add_shape(
        type="line",
        xref="paper",
        x0=0,
        x1=1,
        y0=40,
        y1=40,
        line=dict(dash="5px", color='red'),
    )

    # place a label for the line inside the plot (not in the legend)
    bar.add_annotation(
        xref='paper',
        x=0.99,
        y=40,
        yref='y',
        text='Threshold 40 µg/m³',
        showarrow=False,
        xanchor='right',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='rgba(0,0,0,0.1)',
    )
    return bar.to_html(full_html=False)

def draw_NO2_province_chart():
    dfposts_NO2 = luchtmeetnet_api_fetch_data('NO2')
    dfposts_NO2_province = transform_NO2_province(dfposts_NO2)
    clean_NO2_province_data = clean_NO2_province(dfposts_NO2_province)
    bar_NO2_province_html = create_NO2_province_chart(clean_NO2_province_data)
    print("NO2 province chart created")
    return bar_NO2_province_html


# =======================================================================================
# ---------------------------------------------------------------------------------------
# -------------------------- Draw everything ---------------------------------------------
# ---------------------------------------------------------------------------------------
# =======================================================================================





def draw_measures_chart():
    dfposts_NO2 = luchtmeetnet_api_fetch_data('NO2')
    # dfposts_PM10 = luchtmeetnet_api_fetch_data('PM10')
    # dfposts_PM25 = luchtmeetnet_api_fetch_data('PM2.5')

    meanlocation_clean = clean_NO2_data(dfposts_NO2)
    bar_NO2_clean_html = create_NO2_chart(meanlocation_clean)





    print("Measures chart created")
    return bar_NO2_clean_html