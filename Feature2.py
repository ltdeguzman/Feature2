import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import os
import plotly.express as px
from pathlib import Path
from openai import OpenAI

# URL of the raw CSV file in the GitHub repository
url = 'https://raw.githubusercontent.com/ltdeguzman/Feature2/main/heatmapData.csv'

# Fetch the CSV file content
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load data: {response.status_code}")

# Read the CSV content into a DataFrame
df = pd.read_csv(io.StringIO(response.text))

# Simulate a timestamp column
times = pd.date_range(start='2024-10-27', periods=len(df), freq='H')
df['timestamp'] = times

# Melt the DataFrame to get it into long format suitable for time series plotting
df_melted = df.melt(id_vars=['timestamp'], var_name='aisle', value_name='foot_traffic')

# Title of the heat map table
st.subheader('Heatmap Data of a Retail Store in Downtown San Jose, California', divider='grey')

# Display the DataFrame
st.dataframe(df)

# Create a time series plot for foot traffic
time_chart = px.line(df_melted, x='timestamp', y='foot_traffic', color='aisle', title='Foot Traffic in Aisles Over Store Hours')
st.plotly_chart(time_chart)

# Display the random data for comparison
st.subheader('Other Retail Store Heat Map Data Comparison in Downtown San Jose, California', divider='grey')

random_df = pd.DataFrame(np.random.randn(11, 11), columns=("Aisle %d" % i for i in range(11)))

# Simulate a timestamp column for random data
random_times = pd.date_range(start='2024-10-27', periods=11, freq='H')
random_df['timestamp'] = random_times

# Melt the DataFrame to get it into long format suitable for time series plotting
random_df_melted = random_df.melt(id_vars=['timestamp'], var_name='aisle', value_name='foot_traffic')

# Display the random data
st.dataframe(random_df)

# Create a time series plot for the random data
random_time_chart = px.line(random_df_melted, x='timestamp', y='foot_traffic', color='aisle', title='Random Data Foot Traffic in Aisles Over Store Hours')
st.plotly_chart(random_time_chart)