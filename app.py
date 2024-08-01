# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 17:51:31 2024

@author: hayam
"""


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

# Load the dataset
data_combined = pd.read_csv("combined_data.csv")  # Update this path to your dataset

# Replace NaN values in 'Cause of death or injury' with 'All'
data_combined['Cause of death or injury'].fillna('All', inplace=True)

# Add latitude and longitude coordinates for each location
location_coords = {
    "Afghanistan": [33.93911, 67.709953],
    "Algeria": [28.033886, 1.659626],
    "Bahrain": [26.0667, 50.5577],
    "Egypt": [26.820553, 30.802498],
    "Iran (Islamic Republic of)": [32.4279, 53.6880],
    "Iraq": [33.223191, 43.679291],
    "Jordan": [30.5852, 36.2384],
    "Kuwait": [29.3759, 47.9774],
    "Lebanon": [33.8547, 35.8623],
    "Libya": [26.3351, 17.2283],
    "Morocco": [31.7917, -7.0926],
    "Oman": [21.4735, 55.9754],
    "Palestine": [31.9474, 35.2272],
    "Qatar": [25.3548, 51.1839],
    "Saudi Arabia": [23.8859, 45.0792],
    "Sudan": [12.8628, 30.2176],
    "Syrian Arab Republic": [34.802075, 38.996815],
    "Tunisia": [33.8869, 9.5375],
    "Türkiye": [38.9637, 35.2433],
    "United Arab Emirates": [23.4241, 53.8478],
    "Yemen": [15.552727, 48.516388]
}

data_combined['Latitude'] = data_combined['Location'].apply(lambda x: location_coords.get(x, [0, 0])[0])
data_combined['Longitude'] = data_combined['Location'].apply(lambda x: location_coords.get(x, [0, 0])[1])

# Sidebar for user input
st.sidebar.title("Filter Options")
selected_disease = st.sidebar.selectbox("Select Neurological Disease", ['All'] + list(data_combined['Cause of death or injury'].unique()))
selected_age_group = st.sidebar.selectbox("Select Age Group", ['All'] + list(data_combined['Age'].unique()))
selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + list(data_combined['Sex'].unique()))

# Filter data based on user input
filtered_data = data_combined.copy()

if selected_disease != 'All':
    filtered_data = filtered_data[filtered_data['Cause of death or injury'] == selected_disease]
if selected_age_group != 'All':
    filtered_data = filtered_data[filtered_data['Age'] == selected_age_group]
if selected_gender != 'All':
    filtered_data = filtered_data[filtered_data['Sex'] == selected_gender]

# Visualizations
st.title("Neurological Diseases Analysis")

# Distribution Across Different Neurological Diseases
st.subheader("Distribution of Neurological Diseases")
plt.figure(figsize=(14, 8))
sns.boxplot(data=filtered_data, x='Cause of death or injury', y='Value')
plt.title("Distribution of Neurological Diseases")
plt.xlabel("Neurological Disease")
plt.ylabel("YLDs per 100,000")
plt.xticks(rotation=90)
st.pyplot(plt)

# Distribution Across Age Groups
st.subheader("Distribution Across Age Groups")
if filtered_data['Age'].nunique() > 1:
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=filtered_data, x='Age', y='Value')
    plt.title("Distribution of Neurological Diseases Across Age Groups")
    plt.xlabel("Age Group")
    plt.ylabel("YLDs per 100,000")
    plt.xticks(rotation=90)
    st.pyplot(plt)

# Distribution Across Genders
st.subheader("Distribution Across Genders")
if filtered_data['Sex'].nunique() > 1:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=filtered_data, x='Sex', y='Value')
    plt.title("Distribution of Neurological Diseases Across Genders")
    plt.xlabel("Gender")
    plt.ylabel("YLDs per 100,000")
    st.pyplot(plt)

# Interactive Map
st.subheader("Geographical Distribution of Neurological Diseases")

# Aggregate data by location
aggregated_data = filtered_data.groupby('Location').agg({'Value': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Create a base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add points to the map with radius based on the square root of aggregated 'Value'
for idx, row in aggregated_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=(row['Value']**0.5) * 0.1,  # Use square root to scale better
        popup=f"{row['Location']}: {row['Value']} YLDs per 100,000",
        color='red',
        fill=True,
    ).add_to(m)

# Display the map in Streamlit
folium_static(m)

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_data)
