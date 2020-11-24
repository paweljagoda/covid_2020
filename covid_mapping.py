# covid_mapping.py

import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt
import geopandas as gpd
import os 
from pathlib import Path 
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import StrMethodFormatter
import mapclassify as mc
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pylab as pl
import calendar

data = pd.read_csv('data.csv')

data_select = data.loc[:,['month','year','cases','countriesAndTerritories','continentExp']]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

data_select = data_select.rename(columns={'countriesAndTerritories':'name'})

data_select = data_select.replace('_', ' ', regex=True)

data_select['month'] = data_select['month'].apply(lambda x: calendar.month_abbr[x])

output_path = Path('maps')

def by_month(df, month):
     return df[df['month'] == month]

months = [('00','Dec'), ('01','Jan'), ('02','Feb'), ('03','Mar'), ('04','Apr'), ('05','May'), ('06','Jun'), ('07','Jul'),('08','Aug'), ('09','Sep'),('10','Oct'), ('11','Nov')]

for x, month in months:
     by_month(data_select, month).to_csv(f'{x}_cases_{month}.csv')

list_of_months = [
'00_cases_Dec.csv',
'01_cases_Jan.csv',
'02_cases_Feb.csv',
'03_cases_Mar.csv',
'04_cases_Apr.csv',
'05_cases_May.csv',
'06_cases_Jun.csv',
'07_cases_Jul.csv',
'08_cases_Aug.csv',
'09_cases_Sep.csv',
'10_cases_Oct.csv',
'11_cases_Nov.csv',
]
def generate_plot_of_cases(month):
    
    # load data for particular month
    df = pd.read_csv(month)

    # merge covid case data set with geospacial data
    geo_month = world.merge(df, left_on = 'name', right_on = 'name')

    # create map, added plt.Normalize to keep the legend range the same for all maps
    fig = geo_month.plot(column='cases', 
                        cmap='OrRd', 
                        figsize=(20,10), 
                        linewidth=0.8, 
                        edgecolor='1', 
                        vmin=data.cases.min(), 
                        vmax=data.cases.max(), 
                        legend=False)
                        #norm=plt.Normalize(data.cases.min(), vmax=data.cases.max()))
    
    # remove axis of chart
    fig.axis('off')
    
    # add a title to map
    fig.set_title('Covid Cases Per Month', \
              fontdict={'fontsize': '25',
                         'fontweight' : '3'})
    
    # create and position the Year annotation to the bottom left   
    fig.annotate(month[9:12], xy=(0.1, .225), xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=35)

    # this will save the figure as a high-res png in the output path. 
    filepath = output_path / (month[0:3] + '_' + month[9:12] + '_cases.png')
    chart = fig.get_figure()
    chart.savefig(filepath, dpi=100) # dpi controls the resolution

for month in list_of_months:
     generate_plot_of_cases(month=month)

#months_list = data_select['month'].unique()

#data_april = data_select[data_select['month'] == 4]

#geo_data_april = world.merge(data_april, left_on = 'name', right_on = 'name')

#geoplot.choropleth(geo_data_april, hue='cases', cmap='OrRd', figsize=(8, 4))

#plt.show()