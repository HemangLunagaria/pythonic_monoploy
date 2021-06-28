#!/usr/bin/env python
# coding: utf-8

# # Toronto Dwellings Analysis Dashboard
# 
# In this notebook, you will compile the visualizations from the previous analysis into functions to create a Panel dashboard.

# In[1]:


# imports
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv


# In[2]:


# Initialize the Panel Extensions (for Plotly)
import panel as pn
pn.extension("plotly")


# In[3]:


# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("mapbox")
px.set_mapbox_access_token(map_box_api)


# # Import Data

# In[4]:


# Import the CSVs to Pandas DataFrames
file_path = Path("Data/toronto_neighbourhoods_census_data.csv")
to_data = pd.read_csv(file_path, index_col="year")

file_path = Path("Data/toronto_neighbourhoods_coordinates.csv")
df_neighbourhood_locations = pd.read_csv(file_path)


# - - -

# ## Panel Visualizations
# 
# In this section, you will copy the code for each plot type from your analysis notebook and place it into separate functions that Panel can use to create panes for the dashboard. 
# 
# These functions will convert the plot object to a Panel pane.
# 
# Be sure to include any DataFrame transformation/manipulation code required along with the plotting code.
# 
# Return a Panel pane object from each function that can be used to build the dashboard.
# 
# Note: Remove any `.show()` lines from the code. We want to return the plots instead of showing them. The Panel dashboard will then display the plots.

# ### Global available data

# In[5]:


# Getting the data from the top 10 expensive neighbourhoods
# YOUR CODE HERE!
avg_house_value_by_neighbourhood = to_data.loc[:,['neighbourhood','average_house_value']]
neighbourhoods_value_avg = avg_house_value_by_neighbourhood.reset_index().drop(columns=['year']).groupby(['neighbourhood']).mean()

# Calculate the mean number of dwelling types units per year
# YOUR CODE HERE!
dwelling_types = ['single_detached_house', 'apartment_five_storeys_plus','movable_dwelling', 'semi_detached_house','row_house', 'duplex','apartment_five_storeys_less','other_house']
no_of_dwelling_by_year = to_data.loc[:,dwelling_types].groupby(by='year').sum()

# Calculate the average monthly shelter costs for owned and rented dwellings
# YOUR CODE HERE!
monthly_avg_costs_by_year = to_data.loc[:,['shelter_costs_owned','shelter_costs_rented']].groupby(by='year').mean()
monthly_avg_costs_by_year

avg_house_value = to_data['average_house_value'].groupby(by='year').mean()


# In[6]:


# neighbourhoods_value_avg


# ### Panel Visualization Functions

# In[7]:


# Define Panel visualization functions
def neighbourhood_map():
    df_neighbourhood_locations.set_index('neighbourhood', inplace=True)
    neighbourhood_avg_value_with_location = pd.concat([df_neighbourhood_locations, neighbourhoods_value_avg], axis=1)
    neighbourhood_avg_value_with_location = neighbourhood_avg_value_with_location.reset_index()
    map_plot = px.scatter_mapbox(
        neighbourhood_avg_value_with_location,
        lat="lat",
        lon="lon",
        size="average_house_value",
        color="neighbourhood",
        title = "Average House Values in Toronto",
        zoom=10,
        width=1500,
        height=800
    )
    return map_plot
   
    # YOUR CODE HERE!

def create_bar_chart(data, title, xlabel, ylabel, color):
#     plt.figure()
    plot = data.hvplot.bar(title=title,color=color,xlabel=xlabel, ylabel=ylabel,rot=90, yformatter='$%.2f',height=600, width=800)
#     plot = data.plot.bar(title=title,color=color)
#     plot.set_xlabel(xlabel)
#     plot.set_ylabel(ylabel)
    return plot
    
    # YOUR CODE HERE!

def create_line_chart(data, title, xlabel, ylabel, color):
    return data.hvplot.line(title=title, xlabel=xlabel, ylabel=ylabel, color=color)
    
    # YOUR CODE HERE!

def average_house_value():
    avg_house_value = to_data['average_house_value'].groupby(by='year').mean()
    return avg_house_value.hvplot.line(title='Average House Value in Toronto', xlabel="Year", ylabel="Avg. House Value", yformatter='$%.2f', height=600, width=800)
    # YOUR CODE HERE!

def average_value_by_neighbourhood():
    avg_house_value_by_neighbourhood = to_data.loc[:,['neighbourhood','average_house_value']]
    return avg_house_value_by_neighbourhood.hvplot.line(groupby='neighbourhood', xlabel="Year", ylabel="Avg. House Value", yformatter='$%.2f')
    # YOUR CODE HERE!

def number_dwelling_types():
    column_list = dwelling_types.copy()
    column_list.append('neighbourhood')
    no_of_dwelling_types_per_year_by_neighbourhood = to_data.loc[:,column_list]
    return no_of_dwelling_types_per_year_by_neighbourhood.hvplot.bar(groupby='neighbourhood', rot=90, height=600, width=1000, xlabel='Year', ylabel='Dwelling Type Units')
    # YOUR CODE HERE!

def average_house_value_snapshot():
    avg_house_value_by_year = to_data.loc[:,['neighbourhood', 'average_house_value']].reset_index()

    return px.bar(avg_house_value_by_year, x="neighbourhood", y="average_house_value", color="average_house_value", facet_row="year", width=1700, height=1200, title="Average House Values in Toronto per Neighbourhood", labels={
                     "neighbourhood": "Neighbourhood",
                     "average_house_value": "Avg. House Value",
                     "average_house_value": "Avg. House Value"
                 })

    # YOUR CODE HERE!

def top_most_expensive_neighbourhoods():
    top_10_neighbourhoods_avg = neighbourhoods_value_avg.nlargest(10, 'average_house_value')
    return top_10_neighbourhoods_avg.hvplot.bar(title="Top 10 Expensive Neighbourhoods in Toronto", xlabel="Neighbourhood", ylabel="Avg. House Value", yformatter='$%.2f', rot=90, width=1000, height=600)
    # YOUR CODE HERE!

def sunburts_cost_analysis():
    sunburst_data = to_data.loc[:,['neighbourhood','shelter_costs_owned']].reset_index()
    sunburst_data = sunburst_data.sort_values('shelter_costs_owned',ascending = False).groupby(by=['year'])
    return px.sunburst(sunburst_data.head(10), path=['year', 'neighbourhood'], values='shelter_costs_owned', color='shelter_costs_owned',height=800,width=1200, title='Cost Analysis of Most Expensive Neighbourhoods in Toronto per Year')
    
    # YOUR CODE HERE!


# ## Panel Dashboard
# 
# In this section, you will combine all of the plots into a single dashboard view using Panel. Be creative with your dashboard design!

# In[8]:


# Create a Title for the Dashboard
# YOUR CODE HERE!
title_row = pn.pane.Markdown('# Real Estate Analysis of Toronto from 2001 to 2016')

# Define a welcome text
# YOUR CODE HERE!
welcome_tab = pn.Column('#### This dashboard presents a visual analysis of historical house values, dwelling types per neighbourhood and dwelling costs in Toronto, Ontario according to census data from 2001 to 2016.You can navigate through the tabs above to explore more details about the evolution of the real estate market on the 6 across these years.', neighbourhood_map())

# Create a tab layout for the dashboard
# YOUR CODE HERE!
tabs = pn.Tabs(("Welcome", welcome_tab))

# Create the main dashboard
# YOUR CODE HERE!
yearly_analysis_row1 = pn.Row(create_bar_chart(no_of_dwelling_by_year.loc[2001], "Dwelling Types in Toronto in 2001", "2001", "Dwelling Type Units", "red"),create_bar_chart(no_of_dwelling_by_year.loc[2006], "Dwelling Types in Toronto in 2006", "2006", "Dwelling Type Units", "blue"))
yearly_analysis_row2 = pn.Row(create_bar_chart(no_of_dwelling_by_year.loc[2011], "Dwelling Types in Toronto in 2011", "2011", "Dwelling Type Units", "orange"),create_bar_chart(no_of_dwelling_by_year.loc[2016], "Dwelling Types in Toronto in 2016", "2016", "Dwelling Type Units", "magenta"))
yearly_market_analysis_tab = pn.Column(yearly_analysis_row1, yearly_analysis_row2)

cost_value_comparison_tab = pn.Column(create_line_chart(monthly_avg_costs_by_year["shelter_costs_owned"], "Average Monthly Shelter Cost for Owned Dwellings in Toronto", "Year", "Avg Monthly Shelter Costs", "blue"),create_line_chart(monthly_avg_costs_by_year["shelter_costs_rented"], "Average Monthly Shelter Cost for Rented Dwellings in Toronto", "Year", "Avg Monthly Shelter Costs", "orange"),average_house_value())

neighbourhood_analysis_column = pn.Column(average_value_by_neighbourhood(),number_dwelling_types())
neighbourhood_analysis_tab = pn.Row(neighbourhood_analysis_column, average_house_value_snapshot())

expensive_neighbourhoods_tab = pn.Row(top_most_expensive_neighbourhoods(), sunburts_cost_analysis())

tabs.append(("Yearly Market Analysis", yearly_market_analysis_tab))
tabs.append(('Shelter Costs Vs. House Value', cost_value_comparison_tab))
tabs.append(('Neighbourhood Analysis', neighbourhood_analysis_tab))
tabs.append(('Top Expensive Neighbourhoods', expensive_neighbourhoods_tab))

dashboard = pn.Column(title_row, tabs)
dashboard


# ## Serve the Panel Dashboard

# In[10]:


dashboard.servable()


# # Debugging
# 
# Note: Some of the Plotly express plots may not render in the notebook through the panel functions.
# 
# However, you can test each plot by uncommenting the following code

# In[ ]:


neighbourhood_map().show()


# In[ ]:


# create_bar_chart(data, title, xlabel, ylabel, color)

# # Bar chart for 2001
create_bar_chart(no_of_dwelling_by_year.loc[2001], "Dwelling Types in Toronto in 2001", "2001", "Dwelling Type Units", "red")

# # Bar chart for 2006
# create_bar_chart(df_dwelling_units.loc[2006], "Dwelling Types in Toronto in 2006", "2006", "Dwelling Type Units", "blue")

# # Bar chart for 2011
# create_bar_chart(df_dwelling_units.loc[2011], "Dwelling Types in Toronto in 2011", "2011", "Dwelling Type Units", "orange")

# # Bar chart for 2016
# create_bar_chart(df_dwelling_units.loc[2016], "Dwelling Types in Toronto in 2016", "2016", "Dwelling Type Units", "magenta")


# In[ ]:


# create_line_chart(data, title, xlabel, ylabel, color)

# # Line chart for owned dwellings
# create_line_chart(monthly_avg_costs_by_year["shelter_costs_owned"], "Average Monthly Shelter Cost for Owned Dwellings in Toronto", "Year", "Avg Monthly Shelter Costs", "blue")

# # Line chart for rented dwellings
# create_line_chart(monthly_avg_costs_by_year["shelter_costs_rented"], "Average Monthly Shelter Cost for Rented Dwellings in Toronto", "Year", "Avg Monthly Shelter Costs", "orange")

create_line_chart(avg_house_value,'Average House Value in Toronto','Year','Avg. House Value','blue')
# avg_house_value.hvplot.line(title='Average House Value in Toronto', xlabel="Year", ylabel="Avg. House Value", yformatter='$%.2f')


# In[9]:


average_house_value()


# In[ ]:


# average_value_by_neighbourhood()


# In[ ]:


# number_dwelling_types()


# In[ ]:


# average_house_value_snapshot()


# In[ ]:


# top_most_expensive_neighbourhoods()


# In[ ]:


# sunburts_cost_analysis()

