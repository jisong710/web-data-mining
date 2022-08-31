# -*- coding: utf-8 -*-
"""TA_1103184023_LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19sUFT3crVPES_n-yOjAsWrk3sTk5ksVo

**IMPORT LIBRARY**
"""
import matplotlib
matplotlib.use('Agg')
import io
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import pymysql
import tensorflow as tf
import os
from matplotlib import pyplot
from datetime import datetime, timedelta
from math import sqrt
from numpy import concatenate
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
import base64
from io import BytesIO

class lstm:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", database="machinelearnTBC", charset='utf8mb4')
    def lstm(self):
        df = pd.read_csv('datasetTBC.csv', parse_dates=["date"])
        df

        """# **PreProcessing**"""

        df['date']=  pd.to_datetime(df['date'])

        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        df

        df.info()

        """menbuang data nol"""

        df['date'].fillna(0,inplace = True)
        df = df.loc[df['jumlahpenderita']>0]
        df

        df = df.replace('---', np.nan)
        df

        df.isnull().sum()

        df.dropna(subset = ["date"], inplace=True)
        df

        """# Mengubah data menjadi float"""

        df['jumlahpenderita']=df['jumlahpenderita'].astype(str).astype(float)
        df

        plt.figure(figsize=(20, 8))
        df['jumlahpenderita'].plot(title = 'Original Data', color = 'b')
        plt.show()

        """Membuat Variabel Dataset """

        Dataset = df.copy()

        Dataset = Dataset.set_index('date')
        Dataset .to_csv( "datasettbcclear.csv", encoding='utf-8-sig')
        Dataset

        """Parameter untuk proses training split"""

        DatasetJumlahpenderita = Dataset.copy()

        """Pembagian Train dan Test"""

        DataJP = DatasetJumlahpenderita
        Dataset_Jumlahpenderita = DataJP.values
        training_data_jumlahpenderita=int(np.ceil(len(Dataset_Jumlahpenderita)*.70))
        training_data_jumlahpenderita

        Dataset_Jumlahpenderita = Dataset_Jumlahpenderita.reshape(-1,1)
        Dataset_Jumlahpenderita

        """NORMALISI MINMAX SCALER"""

        scale = MinMaxScaler()
        sca = scale.fit_transform(Dataset_Jumlahpenderita)
        sca

        """Mengubah menjadi 3D array"""

        #Membuat TRAINING DATA
        train_data_JP = sca[0:int(training_data_jumlahpenderita), :]
        #Bagi data x_train dan y_train
        x_train = []
        y_train = []

        for i in range(30,len(train_data_JP)):
            x_train.append(train_data_JP[i-30:i, 0])
            y_train.append(train_data_JP[i, 0])

        #Ubah x_train dan y_train ke Numppy Arrays
        x_train,y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

        """## MODELING"""

        model = Sequential()

        model.add(LSTM(units = 256, return_sequences=False, input_shape= (x_train.shape[1], 1)))
        model.add(Dense(units = 1, activation="sigmoid"))

        # Compile the model
        opt = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(loss='mean_squared_error', optimizer=opt)

        history = model.fit(x_train, y_train, batch_size=100, epochs = 700)

        model.save('Model_JP.h5')

        plt.figure(figsize=(14,6))
        plt.plot(history.history["loss"],label="loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.show()

        """Membuat TEST DATA(y_train x_test y_test"""

        #Membuat DATA TESTING
        test_data_JP = sca[training_data_jumlahpenderita - 30: ,:]
        #Membuat data x_test dan y_test
        x_test_JP = []
        y_test_JP =  sca[training_data_jumlahpenderita:, :]
        for i in range(30,len(test_data_JP)):
            x_test_JP.append(test_data_JP[i-30:i,0])

        #Ubah Data Ke Numpy Array
        x_test_JP = np.array(x_test_JP)

        #
        x_test_JP = np.reshape(x_test_JP, (x_test_JP.shape[0],x_test_JP.shape[1],1))

        #Model Prediksi
        predictions_JP = model.predict(x_test_JP)
        model.reset_states()

        """NILAI ERROR"""

        mae = mean_absolute_error(y_test_JP,predictions_JP)
        mse = mean_squared_error(y_test_JP,predictions_JP)
        rmse = np.sqrt(mse)

        print ('MAE :',mae)
        print ('MSE :',mse)
        print ('RMSE :',rmse)

        """DENORMALISASI"""

        predictions_JP_scale = scale.inverse_transform(predictions_JP)
        predictions_JP_scale

        """PERBANDINGAN TEST DATA DAN PREDIKSI"""

        train_data_JP = DataJP[:training_data_jumlahpenderita]
        valid_data_JP = Dataset[['jumlahpenderita']][training_data_jumlahpenderita:]

        train_data_JP = pd.DataFrame(train_data_JP)
        valid_data_JP = pd.DataFrame(valid_data_JP)
        valid_data_JP['predictions_JP'] = predictions_JP_scale
        valid_data_JP

        valid_data_JP.to_csv( "JP_TESTTINGPREDICT.CSV",encoding='utf-8-sig')

        """VISUALISASI PERBANDINGAN"""

        plt.figure(figsize=(14,6))
        plt.plot(valid_data_JP['jumlahpenderita'],label="validasi",c = "r")
        plt.plot(valid_data_JP['predictions_JP'],label="Prediksi",c="b")
        plt.legend()
        plt.show()

        Dataset_JP = Dataset.copy()

        Dataset_JP = Dataset[['jumlahpenderita']]

        Dataset_JP.info()

        Dataset_JP.reset_index(drop=True)

        inputJP = Dataset_JP[len(Dataset_JP)- len(Dataset_JP) - 45 - 45:].values
        inputJP = inputJP.reshape(-1,1)
        inputJP = scale.transform(inputJP)

        x_test_JP = []
        y_test_JP = []
        for i in range (30, 30 + 30 ):
            x_test_JP.append(inputJP[i-30:i, 0])
        
        
        x_test_JP, y_test_JP = np.array(x_test_JP), np.array(y_test_JP)

        x_test_JP = np.reshape(x_test_JP,(x_test_JP.shape[0], x_test_JP.shape[1],1))
        x_test_JP.shape

        n_future = 30 # Redfening n_future to extend prediction dates beyond original dates .. 
        forecast_period_dates = pd.date_range(start='2022-01-01', periods=n_future, freq='1d').tolist()
        forecast_period_dates[:30]

        forecast = model.predict(x_test_JP[:+n_future])
        forecast.shape

        x_test_JP[:+30].shape

        Dataset_JP.shape[1]

        y_pred_future = scale.inverse_transform(forecast)[:,0]
        y_pred_future
        con = lstm.connect(self)
        # Convert timestamp to date
        forecast_dates = []
        iteration = 0
        for time_i in forecast_period_dates:
            forecast_dates.append(time_i.date())
            cursor = con.cursor()
            cursor.execute("INSERT INTO penderitaLTSM(jumlah,tanggal) VALUES(%s,%s)",
                           (int(y_pred_future[iteration]),time_i.date()))
            con.commit()
            iteration = iteration+1
            
        df_forecast_JP= pd.DataFrame({'date':np.array(forecast_dates), 'jumlahpenderita':y_pred_future})
        df_forecast_JP['date']=pd.to_datetime(df_forecast_JP['date'])
        df_forecast_JP = df_forecast_JP.set_index('date')

        df_forecast_JP
        Dataset_JP['label']='observed'
        df_forecast_JP['label']='predicted'

        a = [Dataset_JP, df_forecast_JP]
        a = pd.concat(a)
        a=pd.concat([Dataset_JP,df_forecast_JP])
        print(a.head())

        plot_forecast_JP = a
        plot_forecast_JP
        
        plt.figure(figsize=(14,8))
        plt.plot(plot_forecast_JP.loc[plot_forecast_JP['label']=='predicted', 'jumlahpenderita'], label= 'prediksi')

        plt.ylabel("JumlahPenderita")
        plt.xlabel("Date")
        plt.legend()
        plt.title("Jumlah Penderita TBC")
        plt.show()
        plt.title("Jumlah Penderita TBC")
        plt.savefig("static/img/ltsm.png", format='png')
        return plot_forecast_JP.loc[plot_forecast_JP['label']=='predicted', 'jumlahpenderita'].astype(int),plot_forecast_JP.loc[plot_forecast_JP['label']=='predicted'].index
