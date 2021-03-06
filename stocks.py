import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

start = '2019-01-01'
end = '2022-05-12'

st.title('Stock Trend Predictor')

user_input = st.text_input('Enter Stock Sticker' , 'AAPL')
df = data.DataReader(user_input , 'yahoo', start, end)

st.subheader('Data from 1st Jan 2019 to 12th May 2022')
st.write(df.describe())

st.subheader('Closing Price vs Time graph')
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close, 'r', label = 'closing prices')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
st.pyplot(fig)

#st.subheader('Closing Price vs Time graph withn 100 days M.A.')
#ma100 = df.Close.rolling(100).mean()
#fig = plt.figure(figsize = (12,6))
#plt.plot(ma100,'b', label = '100 day MA')
#plt.plot(df.Close,'r', label = 'closing prices')
#plt.xlabel('Time')
#plt.ylabel('Price')
#plt.legend()
#plt.show()
#st.pyplot(fig)'''

st.subheader('Closing Price vs Time graph withn 100 and 200 days M.A.')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'b', label = '100 day MA')
plt.plot(ma200, 'y', label = '200 day MA')
plt.plot(df.Close, 'r', label = 'closing prices')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
st.pyplot(fig)

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)


model = load_model(r"C:\Users\Arnav Jha\OneDrive\Desktop\Project1\Stonks\keras_model.h5")

past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

y_predicted = model.predict(x_test)

scaler = scaler.scale_
scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor


st.subheader('Predictions vs Original')
fig2= plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original price')
plt.plot(y_predicted, 'r', label = 'Predicted price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
