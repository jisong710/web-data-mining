from flask import Flask, render_template, request
from module.database import Database

app = Flask(__name__)
db = Database()

@app.route('/',methods = ['POST', 'GET'])
def index():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.login(request.form);
        if(datalogin != "kosong"):
            return render_template('index.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('login.html',style = style)
    else:
        datalogin = db.login(request.form);
        return render_template('index.html',style = style, username = datalogin)

@app.route('/svr',methods = ['POST', 'GET'])
def index():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.login(request.form);
        if(datalogin != "kosong"):
            return render_template('index.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('login.html',style = style)
    else:
        datalogin = db.login(request.form);
        return render_template('index.html',style = style, username = datalogin)

@app.route('/ltsm',methods = ['POST', 'GET'])
def index():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.login(request.form);
        if(datalogin != "kosong"):
            return render_template('index.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('login.html',style = style)
    else:
        datalogin = db.login(request.form);
        return render_template('index.html',style = style, username = datalogin)

@app.route('/about',methods = ['POST', 'GET'])
def index():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.login(request.form);
        if(datalogin != "kosong"):
            return render_template('index.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('login.html',style = style)
    else:
        datalogin = db.login(request.form);
        return render_template('index.html',style = style, username = datalogin)

@app.route('/information',methods = ['POST', 'GET'])
def index():
    style = "style.css"
    if(request.method == 'POST'):
        print(request.form)
        datalogin = db.login(request.form);
        if(datalogin != "kosong"):
            return render_template('index.html',username = datalogin)
        else:
            message = "error saat login"
            return render_template('login.html',style = style)
    else:
        datalogin = db.login(request.form);
        return render_template('index.html',style = style, username = datalogin)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 
