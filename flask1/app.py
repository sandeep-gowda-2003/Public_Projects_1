from flask import *

import firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate("simple_projects/sample_1/flask1/key.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://demo1-71e7b-default-rtdb.firebaseio.com/"})

dbref=db.reference('/')

flsobj=Flask(__name__)

@flsobj.route('/')
def homepage():
    return render_template('index.html')

@flsobj.route('/aboutus')
def about():
    return render_template('about.html')

@flsobj.route('/services')
def services():
    return render_template('services.html')

@flsobj.route('/jobs')
def jobs():
    return render_template('jobs.html')

@flsobj.route('/sign_up',methods=['get','post'])
def signup():
    if(request.form):
        if request.form['password']==request.form['retype_password']:
            i=dbref.get()['iter']
            dbref.child('User'+str(i)).update({'Name':request.form['name'],"email":request.form['email'],'Password':request.form['password']})
            dbref.update({'iter':i+1})
            return render_template('index.html')
        else:
            var1='PASSWORD NOT MATCHED'
            return render_template('sign_up.html',var=var1)
    return render_template('sign_up.html')

@flsobj.route('/sign_in',methods=['get','post'])
def signin():
    dbref.delete()
    if(request.form):
        pas=request.form['pass']
        user=request.form['Sun']
        return render_template('index1.html')
    return render_template('sign_in.html')

if __name__=='__main__':
    flsobj.run(debug=True)