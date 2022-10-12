import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns
import scipy as sp


st.title('NYC Taxi')


DATA = ('NYC_Taxis_Dataset.csv - Copie de nycc.csv')

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
pickup_hour= data["pickup_hour"].unique()
label_selector= st.slider(
    'Select the hours you want to check',
    min_value=0, max_value=23, value=(0, 1))
start,end= label_selector
start= int(start)
end= int(end)
data['pickup_hour']= data['pickup_hour'].astype('int32')
# st.text(data['pickup_hour'].dtypes)
data_hour= data[(data['pickup_hour']>= start)& (data['pickup_hour']<= end)]
hist_hour = np.histogram(data_hour['pickup_hour'], bins=24, range=(0,24))[0]
st.bar_chart(hist_hour)

# Pyplot Pickups by Weeks
st.subheader('Number of pickups by week day')
data['day_of_week']= data['day_of_week'].astype('int32')

days_list= data["day_of_week"].unique()
day_multi= st.multiselect('kindly add days you want to check:',
             options= days_list)
# st.write(data['day_of_week'])
hist_week=pd.DataFrame()
for i in day_multi:
    hist_week = data[data["day_of_week"]== i]['day_of_week']
# st.write(hist_week)
# st.write(type(day_multi))
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
