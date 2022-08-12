# -*- coding: utf-8 -*-
"""svr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1egoXXyeVTSTN7vZvO0oURDvZwC6GW-zM
"""

#Library
import base64
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import seaborn as sns
import sklearn 
import datetime
from matplotlib import pyplot as plt
from sklearn import preprocessing as pre
from sklearn import svm,preprocessing 
from sklearn.preprocessing import RobustScaler, MinMaxScaler, StandardScaler
from sklearn.model_selection import ShuffleSplit, cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn.svm import SVR
from datetime import datetime, timedelta
import io

class svr:
  def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", database="machinelearnTBC", charset='utf8mb4')
  def svr(self):
    #import dataset
    datatbc = pd.read_csv("datasetTBC.csv")
    datatbc

    """# **PreProcessing**"""

    #mengubah type data "date" (string) menjadi datetime
    datatbc['date']= pd.to_datetime(datatbc['date'])

    # type data "date" di konversi ke datetime
    datatbc['date'] = datatbc['date'].dt.strftime('%Y-%m-%d')

    #membuang nilai nan atau null
    datatbc['date'].fillna(0, inplace = True)

    datatbc = datatbc.loc[datatbc['jumlahpenderita'] > 0]
    datatbc

    #mengubah type data "jumlah penderita" dari int menjadi float
    datatbc['jumlahpenderita']= datatbc['jumlahpenderita'].astype(str).astype(float)
    datatbc

    #menginterpolasi dataset
    datatbc= datatbc.interpolate(method='linear',axis=0)
    datatbc

    datatbc.isnull().sum()

    datatbc["date"] = pd.to_datetime(datatbc["date"])

    datatbc[['date','jumlahpenderita']]
    datatbc.info()

    """# **Train/Test Data**"""

    x = datatbc.mean(axis = 1)
    x = np.reshape(x.values, (len(x),1)) 
    scaler = MinMaxScaler(feature_range=(0, 1))
    print(x)
    x= scaler.fit_transform(x)
    train_size = int(len(x) * 0.5) 
    test_size = len(x) - train_size
    train_data, test_data = x[0:train_size:], x[train_size:len(x):]
    train_data, test_data

    data_x, data_y = [], []
    for i in range(len(train_data)-2):
      a = train_data[i:(i+1), 0]
      data_x.append(a)
      data_y.append(train_data[i + 1, 0])
      print([data_x, data_y, train_data])

    x_train, y_train = np.array(data_x), np.array(data_y)
    x_train, y_train

    data_x, data_y = [], []
    for i in range(len(test_data)-2):
      a = test_data[i:(i+1), 0]
      data_x.append(a)
      data_y.append(test_data[i + 1, 0])
    x_test, y_test = np.array(data_x), np.array(data_y)
    x_test, y_test

    """# **Modelling**"""

    parameters = {'kernel': ('linear', 'rbf', 'poly'), 'C':[ 0.01,0.1,1,10,100], 'gamma': [0.01, 0.05, 0.2, 0.5, 1], 'epsilon': [0.01,0.1,1,10,100]}
    print('prepare params')

    svr = svm.SVR(verbose=True)

    clf = GridSearchCV(svr, parameters, verbose=4)

    print('mulai training')
    train_hasil = clf.fit(x_train, y_train)

    clf.best_params_

    y_predict = train_hasil.predict(x_test)

    plt.subplots(figsize=(10, 5))
    plt.plot(y_test, label = 'test', linewidth = 1.5)
    plt.plot(y_predict, label = "prediksi")
    plt.title("Perbandingan prediksi dengan test")
    plt.xlabel('jumlah data')
    plt.ylabel('jumlahpenderita')
    plt.legend()
    plt.show()

    x = x_train.tolist() + x_test.tolist()
    y = y_train.tolist() + y_test.tolist()
    plt.subplots(figsize=(10, 5))
    plt.plot(y, label = 'test',linewidth = 1.5)
    plt.plot(clf.predict(x), label = 'Prediksi', linewidth = 1.5)
    plt.title("Prediksi tbc")
    plt.xlabel('jumlah data')
    plt.ylabel('jumlahpenderita')
    plt.legend()
    plt.show()

    mae = mean_absolute_error(y_test,y_predict)
    mse = mean_squared_error(y_test,y_predict)
    rmse = np.sqrt(mse)
    print('MAE :', mae)
    print('RMSE :', rmse)
    print('MSE :', mse)

    hasil= pd.DataFrame()
    hasil["ACTUAL"] = y_test.flatten()
    hasil["PREDIKSI"] = y_predict
    hasil

    result = clf.predict(x_test[:+len(x_test)])
    result = result.reshape(-1,1)
    result

    result = scaler.inverse_transform(result)[:,0]
    result

    date_format = "%Y-%m-%d"
    date_list = datatbc['date'].values
    last_date = date_list[-1]
    day = 30
    predict_dates = pd.date_range(start=last_date, periods=day, freq='1d').tolist()

    n = []
    for d in predict_dates:
      n.append(d.date())

    df_predict = pd.DataFrame({'date':np.array(n), 'jumlahpenderita':result[0:len(n)]})
    df_predict['date']=pd.to_datetime(df_predict['date'])
    df_predict = df_predict.set_index('date')
    df_predict

    df_predict.to_csv('SVRjumlahperita.csv', index=True)

    df_predict = pd.read_csv('SVRjumlahperita.csv')
    df_predict

    df_predict.to_csv('SVRPredict.csv')

    df_predict = df_predict.set_index(['date'])
    df_predict.index = pd.to_datetime(df_predict.index)
    df_perday = df_predict.resample('D').max() 

    df_perday

    days= df_predict['jumlahpenderita'].values.tolist()

    days.pop()
    days = [0] + days
    df_perday['jumlahpenderita'] = days

    jumlahpenderita = df_predict['jumlahpenderita'].values.tolist()
    n = []
    for i, k in enumerate(jumlahpenderita):
        if i == 0:
          n.append(0)
        else:
          n.append(k - days[i])
    df_predict

    jumlah  = df_perday['jumlahpenderita']
    print(jumlah)

    df_perday.to_csv('SVRhari.csv')

    datatbc
    datatbc['label']='observed'
    df_predict['label']='prediksi'
    d = [datatbc, df_predict]
    d = pd.concat(d)
    d = pd.concat([datatbc,df_predict])
    d
    svrjpg = io.BytesIO()
    plt.figure(figsize=(15,10))
    plt.plot(d.loc[d['label']=='prediksi', 'jumlahpenderita'], label= 'prediksi', color= 'red')
    plt.ylabel("jumlah penderita penyakit tbc")
    plt.xlabel("Year")
    plt.legend()
    plt.title("Prediksi Penderita Penyakit Tuberkulosis Kab.Karawang")
    plt.savefig("static/img/svr.png", format='png')
    return df_predict['jumlahpenderita'],df_predict.index