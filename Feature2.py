import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import os
import plotly.express as px  # type: ignore
from pathlib import path
import openai

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

# Determine promotion placement by finding the aisle with the highest foot traffic for each timestamp
df['Promotion_Placement'] = df.drop(columns=['timestamp']).idxmax(axis=1)

# Melt the DataFrame to get it into long format suitable for time series plotting
df_melted = df.melt(id_vars=['timestamp'], var_name='aisle', value_name='foot_traffic')

# Filter the data to only include rows where the aisle is the suggested Promotion_Placement
promotion_data = df_melted[df_melted.apply(lambda row: row['aisle'] == df.loc[df['timestamp'] == row['timestamp'], 'Promotion_Placement'].values[0], axis=1)]

# Title of the heat map table
st.subheader('Heatmap Data of a Retail Store in Downtown San Jose, California', divider='grey')

# Display the DataFrame without the Promotion Placement column
st.dataframe(df.drop(columns=['Promotion_Placement']))

# Create a time series plot for foot traffic, including promotion placement
time_chart = px.line(df_melted, x='timestamp', y='foot_traffic', color='aisle', title='Foot Traffic in Aisles Over Store Hours')

# Add promotion placement line to the plot
time_chart.add_scatter(x=promotion_data['timestamp'], y=promotion_data['foot_traffic'], mode='lines+markers', name='Promotion Placement', line=dict(dash='dash'))

# Display the chart
st.plotly_chart(time_chart)

# Display the random data for comparison
st.subheader('Other Retail Store Heat Map Data Comparison in Downtown San Jose, California', divider='grey')

# Generate random data for comparison and add promotion placement suggestion
random_df = pd.DataFrame(np.random.randn(11, 11), columns=("Aisle %d" % i for i in range(11)))
random_times = pd.date_range(start='2024-10-27', periods=11, freq='H')
random_df['timestamp'] = random_times

# Add a promotion placement column for the random data by identifying the highest foot traffic aisle
random_df['Promotion_Placement'] = random_df.drop(columns=['timestamp']).idxmax(axis=1)

# Melt the DataFrame to get it into long format suitable for time series plotting
random_df_melted = random_df.melt(id_vars=['timestamp'], var_name='aisle', value_name='foot_traffic')

# Filter the random data to include only promotion placement aisles
random_promotion_data = random_df_melted[random_df_melted.apply(lambda row: row['aisle'] == random_df.loc[random_df['timestamp'] == row['timestamp'], 'Promotion_Placement'].values[0], axis=1)]

# Display the random data without the Promotion Placement column
st.dataframe(random_df.drop(columns=['Promotion_Placement']))

# Create a time series plot for the random data, including promotion placement
random_time_chart = px.line(random_df_melted, x='timestamp', y='foot_traffic', color='aisle', title='Random Data Foot Traffic in Aisles Over Store Hours')

# Add promotion placement line to the random data plot
random_time_chart.add_scatter(x=random_promotion_data['timestamp'], y=random_promotion_data['foot_traffic'], mode='lines+markers', name='Promotion Placement', line=dict(dash='dash'))

# Display the random data plot
st.plotly_chart(random_time_chart)
