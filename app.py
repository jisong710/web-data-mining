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
    if(request.method == 'POST'):
        plot,tabel = algoritmasvr.svr()
        return render_template('SVR.html')
    else:
        return render_template('SVR.html')

@app.route('/ltsm',methods = ['POST', 'GET'])
def ltsm():
    if(request.method == 'POST'):
        plot,tabel = algoritmalstm.lstm()
        return render_template('LTSM.html')
    else:
        return render_template('LTSM.html')

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
 
