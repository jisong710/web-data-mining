from flask import Flask, render_template, request
from module.lstm import lstm
from module.svr import svr

app = Flask(__name__)
algoritmalstm = lstm()
algoritmasvr = svr()
@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('halamanUtama.html')

@app.route('/svr',methods = ['POST', 'GET'])
def svr():
    tabel = []
    prediksi = []
    if(request.method == 'POST'):
        tabel,prediksi = algoritmasvr.svr()
    length = len(tabel)
    return render_template('SVR.html', tabel = tabel , length = length, predict = prediksi)

@app.route('/lstm',methods = ['POST', 'GET'])
def lstm():
    tabel = []
    prediksi = []
    if(request.method == 'POST'):
        tabel,prediksi = algoritmalstm.lstm()
    length = len(tabel)
    return render_template('LSTM.html', tabel = tabel , length = length, predict = prediksi)

@app.route('/about',methods = ['POST', 'GET'])
def about():
    return render_template('tentangkami.html')

@app.route('/information',methods = ['POST', 'GET'])
def information():
    return render_template('informasialgoritma.html')

@app.route('/dataset',methods = ['POST', 'GET'])
def dataset():
    return render_template('datasetTBC.csv')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 
