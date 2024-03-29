from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint
from pymongo import Connection


app_map = Blueprint('app_map',__name__,template_folder='templates')


@app_map.route('/gmap',methods=['POST','GET'])
def gmap():
    db = Connection("localhost",27017).nano
    online = db.online

    names =["mouse","cat","cow","pig","dog" ,"snake","dragon","sheep","cock","tiger","rabit"]
    if session["uid"]:
        return render_template("index.html",uid=session["uid"],names=names)
    else:
        return redirect(url_for('app_login.login'))


@app_map.route('/talk')
def talk():
    return render_template("talk.html")

@app_map.route('/taskdetail')
def taskdetail():
    return render_template("task_detail.html")
