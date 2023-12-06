import time

from flask import Flask,render_template,request,session,make_response, jsonify,redirect,url_for
import mysql.connector
import numpy as np
import pandas as pd
# import serial
from datetime import datetime
global loadedmodel
global forecast
import pickle
import time
import pandas_ta as pta
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier



db=mysql.connector.connect(user='root',password='',database='bitcoin',port=3306)
cur=db.cursor()

app=Flask(__name__)
app.secret_key="!@wehjbeywe5425c456scjsuywiydbwbqwgdq)(U#*(WJh8uchQ&*Y*)3jnchdsbc"
df = pd.read_csv('DATASET/bitcoin.csv', index_col=False)

global model
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin',methods=['POST','GET'])
def signin():
    print('Rupesh')
    if request.method=='POST':
        email=request.form['email']
        session['useremail']=email
        password=request.form['password']
        sql="select name,password from bitcoinreg where email='%s' and password='%s'"%(email,password)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data==[]:
            msg="Invalid Credentials"
            return render_template('signin.html',msg=msg)
        else:
            return render_template('userhome.html')
    return render_template('signin.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirmpassword=request.form['confirmpassword']
        if password == confirmpassword:
            sq="select * from bitcoinreg where email='%s'"%(email)
            cur.execute(sq)
            data=cur.fetchall()
            db.commit()
            if data==[]:
                sql="insert into bitcoinreg(name,email,password)values(%s,%s,%s)"
                val=(name,email,password)
                cur.execute(sql,val)
                db.commit()
                msg="Data Inserted Successfully"
                return render_template('signup.html',mag=msg)
            elif data !=[]:
                msg="Details already exist"
                return render_template('signup.html',msg=msg)
    return render_template('signup.html')

@app.route('/userprofile')
def userprofile():
    sql="select * from bitcoinreg where email='%s'"%(session['useremail'])
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    data=[j for i in data for j in i]
    val=data[0]
    name=data[1]
    email=data[2]
    Bitcoins=data[3]
    return render_template('userprofile.html',id=val,name=name,email=email,Bitcoins=Bitcoins)

@app.route('/dashboard')
def dashboard():

    price = df.iloc[:, -4]
    time = df.iloc[:,1]

    data = {'time': time.to_dict(), 'price': price.to_dict()}
    return jsonify(data)



@app.route('/storebitcoin')
def storebitcoin():
    buy = request.args.get('buy')
    print(buy)
    sell = request.args.get('sell')
    print(sell)
    bitcoin = int(float(sell)) - int(float(buy))

    sql="select bitcoins from bitcoinreg where email='%s'"%(session['useremail'])
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    coins=data[0][0]
    coins=int(coins)
    print("previous coins :", coins)
    totalcoins=coins + bitcoin
    print('total coins :',totalcoins)
    sql="update bitcoinreg set bitcoins='%s' where email='%s'"%(totalcoins,session['useremail'])
    cur.execute(sql)
    db.commit()
    return 'hello'

@app.route('/dashboard1')
def dashboard1():
    email=session['useremail']
    data = pd.read_csv('DATASET/bitcoin.csv')
    rsi = pta.rsi(data['Close'], length=10)
    data['rsi'] = rsi
    data['ma'] = data.Close.rolling(window=11).mean()
    l = []
    for x in range(data.shape[0]):
        if x >= 10:
            d1 = data.iloc[x, 5]
            d2 = data.iloc[x - 10, 5]
            if d1 > d2:
                l.append('uptrend')
            else:
                l.append('downtrend')
        else:
            l.append('0')
    data['trend'] = pd.DataFrame({'col': l})
    df = data.iloc[10:, :]
    df1 = df.drop('ID', axis=1)
    df1.to_csv('bitcoin_class.csv')
    X = df1.iloc[:, :-1]
    y = df1.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)
    classifier_rf = RandomForestClassifier(random_state=42, n_jobs=-1, max_depth=5, n_estimators=100, oob_score=True)

    classifier_rf.fit(X_train, y_train)
    y_pred = classifier_rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("-------------------------------")
    print(acc)
    print("-------------------------------")
    return render_template("dashboard1.html", email=email, accuracy=acc)





@app.route('/prediction')
def prediction():
    global forecast
    pred = int(request.args.get('sell'))
    print("pred  :: ",pred)
    newdata=df.iloc[pred,1:-1]
    newdata = [newdata]
    print("New Data :", newdata)
    model = pickle.load(open('static/finalized_model.sav', 'rb'))
    print("Model :",model)
    y_pred = model.predict(newdata)
    print("y_pred :: ",y_pred)
    return jsonify({'pred': y_pred[0]})



@app.route('/logout')
def logout():
    try:
        session.pop('useremail',None)
        session.clear()
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True,port='8000')
