from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint
from pymongo import Connection

app_login = Blueprint('app_login',__name__,template_folder='templates')

@app_login.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        print "run into post"
        name = request.form["email"]
        passwd = request.form["password"]
        db = Connection("localhost",27017).nano
        user = db.user
        #u = db.user.find_one({"_id":name,"password":passwd})
        if name:
            if passwd:
                try:
                    user.insert({"_id":name,"password":passwd})
                    return redirect(url_for('login'))
                except:
                    pass
            else:
               pass
        else:
            pass
    return render_template("register.html")


@app_login.route('/login',methods=['POST','GET'])
def login():
    print "run into login"
    if request.method == 'POST':
        print "run here !!"
        db = Connection("localhost",27017).nano
        user = db.user
        name = request.form["email"]
        print name
        passwd = request.form["password"]
        
        print "run ito login part!"
        user = db.user
        u = db.user.find_one({"_id":name})
        if u:
            if u["password"] == passwd:
                session["uid"]=name       
                print session["uid"]
                return redirect(url_for('app_login.firstpage'))     
            else:
                pass
        else:
            pass                
    return render_template("login.html")

@app_login.route('/firstpage',methods=['POST','GET'])
def firstpage():
    return render_template('firstpage.html')

        

@app_login.route('/logout')
def logout():
    session['uid'] = None
    return redirect(url_for('app_login.login'))



