import pandas as pd
import matplotlib.pyplot as plt

def format_monthly_no2_average():

    df_NO2 = pd.read_csv(r"..\..\..\data\ProcessedData\mean_no2_monthlyvalues.csv")

    graph = df_NO2.plot('Year_Month', 'Average NO2 Value')
    graph.set_title("Monthly National Average NO2 Levels")
    graph.set_xlabel("Month")
    graph.set_ylabel("Average NO2 Value (µg/m³)")
    graph.axhline(y=40, color='red', linestyle=':', linewidth=3, label='Max security value 40 µg/m³')
    graph.legend()

def show_monthly_no2_average():
    graph = format_monthly_no2_average()
    return graph.() #add to html function

show_monthly_no2_average()
