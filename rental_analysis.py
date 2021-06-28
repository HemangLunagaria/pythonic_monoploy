#!/usr/bin/env python
# coding: utf-8

# # Toronto Dwellings Analysis
# 
# In this assignment, you will perform fundamental analysis for the Toronto dwellings market to allow potential real estate investors to choose rental investment properties.

# In[1]:


# imports with pyvizenv environment
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


# imports with root environment
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from pathlib import Path


# In[3]:


# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("mapbox")


# ## Load Data

# In[4]:


# Read the census data into a Pandas DataFrame
file_path = Path("Data/toronto_neighbourhoods_census_data.csv")
to_data = pd.read_csv(file_path, index_col="year")
to_data.head()


# - - - 

# ## Dwelling Types Per Year
# 
# In this section, you will calculate the number of dwelling types per year. Visualize the results using bar charts and the Pandas plot function. 
# 
# **Hint:** Use the Pandas `groupby` function.
# 
# **Optional challenge:** Plot each bar chart in a different color.

# In[5]:


# Calculate the sum number of dwelling types units per year (hint: use groupby)
# YOUR CODE HERE!
dwelling_types = ['single_detached_house', 'apartment_five_storeys_plus','movable_dwelling', 'semi_detached_house','row_house', 'duplex','apartment_five_storeys_less','other_house']
no_of_dwelling_by_year = to_data.loc[:,dwelling_types].groupby(by='year').sum()
no_of_dwelling_by_year.head()

index_list = no_of_dwelling_by_year.index.values.tolist()


# In[6]:


# Save the dataframe as a csv file
# YOUR CODE HERE!

no_of_dwelling_by_year.to_csv('Data/sum_of_dwelling_by_year.csv')


# In[15]:


# Helper create_bar_chart function
def create_bar_chart(data, title, xlabel, ylabel, color):
    plt.figure(figsize=(10,8))
    plot = data.plot.bar(title=title,color=color)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)
    plt.show()


# In[16]:


# Create a bar chart per year to show the number of dwelling types

ylabel = "Dwelling type Units"
# Bar chart for 2001
# YOUR CODE HERE!
create_bar_chart(no_of_dwelling_by_year[no_of_dwelling_by_year.index == index_list[0]].iloc[0], "Dwelling Types in Toronto in " + str(index_list[0]), index_list[0], ylabel, "red")

# Bar chart for 2006
# YOUR CODE HERE!
create_bar_chart(no_of_dwelling_by_year[no_of_dwelling_by_year.index == index_list[1]].iloc[0], "Dwelling Types in Toronto in " + str(index_list[1]), index_list[1], ylabel, "blue")

# Bar chart for 2011
# YOUR CODE HERE!
create_bar_chart(no_of_dwelling_by_year[no_of_dwelling_by_year.index == index_list[2]].iloc[0], "Dwelling Types in Toronto in " + str(index_list[2]), index_list[2], ylabel, "orange")

# Bar chart for 2016
# YOUR CODE HERE!
create_bar_chart(no_of_dwelling_by_year[no_of_dwelling_by_year.index == index_list[3]].iloc[0], "Dwelling Types in Toronto in " + str(index_list[3]), index_list[3], ylabel, "purple")


# - - - 

# ## Average Monthly Shelter Costs in Toronto Per Year
# 
# In this section, you will calculate the average monthly shelter costs for owned and rented dwellings and the average house value for each year. Plot the results as a line chart.
# 
# **Optional challenge:** Plot each line chart in a different color.

# In[17]:


# Calculate the average monthly shelter costs for owned and rented dwellings
# YOUR CODE HERE!
monthly_avg_costs_by_year = to_data.loc[:,['shelter_costs_owned','shelter_costs_rented']].groupby(by='year').mean()
monthly_avg_costs_by_year


# In[18]:


# Helper create_line_chart function
def create_line_chart(data, title, xlabel, ylabel, color):
    return data.hvplot.line(title=title, xlabel=xlabel, ylabel=ylabel, color=color)


# In[19]:


# Create two line charts, one to plot the monthly shelter costs for owned dwelleing and other for rented dwellings per year

# Line chart for owned dwellings
# YOUR CODE HERE!
plot_owned = create_line_chart(monthly_avg_costs_by_year['shelter_costs_owned'], 'Average Monthly Shelter Cost for Owned Dwellings in Toronto', 'Year', 'Avg Monthly Shether Costs', 'blue')

# Line chart for rented dwellings
# YOUR CODE HERE!
plot_rented = create_line_chart(monthly_avg_costs_by_year['shelter_costs_rented'], 'Average Monthly Shelter Cost for Rented Dwellings in Toronto', 'Year', 'Avg Monthly Shether Costs', 'orange')
plot_owned + plot_rented


# ## Average House Value per Year
# 
# In this section, you want to determine the average house value per year. An investor may want to understand better the sales price of the rental property over time. For example, a customer will want to know if they should expect an increase or decrease in the property value over time so they can determine how long to hold the rental property. You will visualize the `average_house_value` per year as a bar chart.

# In[35]:


# Calculate the average house value per year
# YOUR CODE HERE!
avg_house_value = to_data['average_house_value'].groupby(by='year').mean()
avg_house_value


# In[21]:


# Plot the average house value per year as a line chart
# YOUR CODE HERE!
avg_house_value.hvplot.line(title='Average House Value in Toronto', xlabel="Year", ylabel="Avg. House Value", yformatter='$%.2f')


# - - - 

# ## Average House Value by Neighbourhood
# 
# In this section, you will use `hvplot` to create an interactive visualization of the average house value with a dropdown selector for the neighbourhood.
# 
# **Hint:** It will be easier to create a new DataFrame from grouping the data and calculating the mean house values for each year and neighbourhood.

# In[22]:


# Create a new DataFrame with the mean house values by neighbourhood per year
# YOUR CODE HERE!
avg_house_value_by_neighbourhood = to_data.loc[:,['neighbourhood','average_house_value']]


# In[23]:


# Use hvplot to create an interactive line chart of the average house value per neighbourhood
# The plot should have a dropdown selector for the neighbourhood
# YOUR CODE HERE!
avg_house_value_by_neighbourhood.hvplot.line(groupby='neighbourhood', xlabel="Year", ylabel="Avg. House Value", yformatter='$%.2f')


# ## Number of Dwelling Types per Year
# 
# In this section, you will use `hvplot` to create an interactive visualization of the average number of dwelling types per year with a dropdown selector for the neighbourhood.

# In[24]:


# Fetch the data of all dwelling types per year
# YOUR CODE HERE!
column_list = dwelling_types.copy()
column_list.append('neighbourhood')
no_of_dwelling_types_per_year_by_neighbourhood = to_data.loc[:,column_list]


# In[25]:


# Use hvplot to create an interactive bar chart of the number of dwelling types per neighbourhood
# The plot should have a dropdown selector for the neighbourhood
# YOUR CODE HERE!
no_of_dwelling_types_per_year_by_neighbourhood.hvplot.bar(groupby='neighbourhood', rot=90, height=600, width=1000, xlabel='Year', ylabel='Dwelling Type Units')


# - - - 

# ## The Top 10 Most Expensive Neighbourhoods
# 
# In this section, you will need to calculate the house value for each neighbourhood and then sort the values to obtain the top 10 most expensive neighbourhoods on average. Plot the results as a bar chart.

# In[26]:


# Getting the data from the top 10 expensive neighbourhoods
# YOUR CODE HERE!
neighbourhoods_value_avg = avg_house_value_by_neighbourhood.reset_index().drop(columns=['year']).groupby(['neighbourhood']).mean()
top_10_neighbourhoods_avg = neighbourhoods_value_avg.nlargest(10, 'average_house_value')
top_10_neighbourhoods_avg


# In[27]:


# Plotting the data from the top 10 expensive neighbourhoods
# YOUR CODE HERE!
top_10_neighbourhoods_avg.hvplot.bar(title="Top 10 Expensive Neighbourhoods in Toronto", xlabel="Neighbourhood", ylabel="Avg. House Value", rot=90, width=1000, height=600)


# - - - 

# ## Neighbourhood Map
# 
# In this section, you will read in neighbourhoods location data and build an interactive map with the average house value per neighbourhood. Use a `scatter_mapbox` from Plotly express to create the visualization. Remember, you will need your Mapbox API key for this.

# ### Load Location Data

# In[28]:


# Load neighbourhoods coordinates data
file_path = Path("Data/toronto_neighbourhoods_coordinates.csv")
df_neighbourhood_locations = pd.read_csv(file_path)
df_neighbourhood_locations.set_index('neighbourhood', inplace=True)
df_neighbourhood_locations.head()


# ### Data Preparation
# 
# You will need to join the location data with the mean values per neighbourhood.
# 
# 1. Calculate the mean values for each neighbourhood.
# 
# 2. Join the average values with the neighbourhood locations.

# In[29]:


# Calculate the mean values for each neighborhood
# YOUR CODE HERE!
# Average value calculated above
neighbourhoods_value_avg.head()


# In[30]:


# Join the average values with the neighbourhood locations
# YOUR CODE HERE!
neighbourhood_avg_value_with_location = pd.concat([df_neighbourhood_locations, neighbourhoods_value_avg], axis=1)
neighbourhood_avg_value_with_location = neighbourhood_avg_value_with_location.reset_index()
neighbourhood_avg_value_with_location.head()


# ### Mapbox Visualization
# 
# Plot the average values per neighbourhood using a Plotly express `scatter_mapbox` visualization.

# In[31]:


# Create a scatter mapbox to analyze neighbourhood info
# YOUR CODE HERE!
px.set_mapbox_access_token(map_box_api)

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

map_plot.show()


# - - -

# ## Cost Analysis - Optional Challenge
# 
# In this section, you will use Plotly express to a couple of plots that investors can interactively filter and explore various factors related to the house value of the Toronto's neighbourhoods. 
# 
# ### Create a bar chart row facet to plot the average house values for all Toronto's neighbourhoods per year

# In[32]:


# YOUR CODE HERE!
avg_house_value_by_year = to_data.loc[:,['neighbourhood', 'average_house_value']].reset_index()

px.bar(avg_house_value_by_year, x="neighbourhood", y="average_house_value", color="average_house_value", facet_row="year", width=1700, height=1200, title="Average House Values in Toronto per Neighbourhood", labels={
                     "neighbourhood": "Neighbourhood",
                     "average_house_value": "Avg. House Value",
                     "average_house_value": "Avg. House Value"
                 })


# ### Create a sunburst chart to conduct a costs analysis of most expensive neighbourhoods in Toronto per year

# In[33]:


# Fetch the data from all expensive neighbourhoods per year.
# YOUR CODE HERE!
sunburst_data = to_data.loc[:,['neighbourhood','shelter_costs_owned']].reset_index()
sunburst_data = sunburst_data.sort_values('shelter_costs_owned',ascending = False).groupby(by=['year'])
sunburst_data.head()


# In[34]:


# Create the sunburst chart
# YOUR CODE HERE!
px.sunburst(sunburst_data.head(10), path=['year', 'neighbourhood'], values='shelter_costs_owned', color='shelter_costs_owned',height=800,width=1200, title='Cost Analysis of Most Expensive Neighbourhoods in Toronto per Year')


# In[ ]:




