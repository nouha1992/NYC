#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns
import scipy as sp


st.title('NYC Taxi')


DATA = ('/Users/nouna/Desktop/NYC_Taxis_Dataset.csv - Copie de nycc.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data["pickup_datetime"] = pd.to_datetime(data.pickup_datetime, format='%Y-%m-%d %H:%M:%S')
    data["pickup_hour"] = data["pickup_datetime"].dt.hour
    data["day_of_week"] = data["pickup_datetime"].dt.dayofweek
    data["pickup_month"] = data["pickup_datetime"].dt.month
    data["pickup_year"] = data["pickup_datetime"].dt.year
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
    
#Bar Chart Pickup by Hours

st.subheader('Number of pickups by hour')
hist_hour = np.histogram(data["pickup_hour"], bins=24, range=(0,24))[0]
st.bar_chart(hist_hour)

# Pyplot Pickups by Weeks
st.subheader('Number of pickups by week')
hist_week = data["day_of_week"]
fig, ax = plt.subplots()
ax.hist(hist_week, bins=7, range=(0,7))[0]
st.pyplot(fig)


#st.subheader('Number of pickups by week')
#hist_week = np.histogram(data["day_of_week"], bins=7, range=(0,7))[0]
#st.bar_chart(hist_week)

#Line Chart Pickups by Month
st.subheader('Number of pickups by month')
hist_month = np.histogram(data["pickup_month"], bins=12, range=(0,12))[0]
st.line_chart(hist_month)


#Plotly Charts
st.subheader('Trips Amounts')
hist_data= [data["tip_amount"], data["total_amount"], data["fare_amount"]]
group_labels = ['Tips Amount', 'Total Amount', 'Fare Amount']
fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, 0.5])
st.plotly_chart(fig, use_container_width=True)


