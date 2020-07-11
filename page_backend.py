from flask import Flask, render_template, redirect, url_for, request
import os,sys
from sqlconnect import check_user

app=Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('processing')
        #insert code here
        user=request.form['username']
        pwd=request.form['password']
        if(check_user(user,pwd))
        {
        	
        }


    return render_template('login_form.html')
if __name__=='__main__':
    app.run(debug=True,port=3333)