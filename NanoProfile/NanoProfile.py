from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint
from pymongo import Connection

app_person = Blueprint('app_person',__name__,template_folder='templates')

@app_person.route('/personinfo',methods=['POST','GET'])
def personinfo():
    return render_template('personinfo.html')
