from flask import Flask,render_template,session,url_for,request,redirect
from pymongo import Connection
# -*- coding: utf-8 -*-
from login.login import app_login
from Nanomap.nanomap import app_map
from NanoProfile.NanoProfile import app_person

app=Flask(__name__)

#define the key:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(app_login,url_prefix='/login')
app.register_blueprint(app_map,url_prefix='/gmap')
app.register_blueprint(app_person,url_prefix='/profile')

"""
@app.route('/gmap',methods=['POST','GET'])
def gmap():
    db = Connection("localhost",27017).nano
    online = db.online

    names =["mouse","cat","cow","pig","dog" ,"snake","dragon","sheep","cock","tiger","rabit"]
    if session["uid"]:
        return render_template("index.html",uid=session["uid"],names=names)
    else:
        return redirect(url_for('login'))

@app.route('/talk')
def talk():
    return render_template("talk.html")


@app.route('/login',methods=['POST','GET'])
def login():
    print "run into login"
    if request.method == 'POST':
        print "run here !!"
        db = Connection("localhost",27017).nano
        user = db.user
        name = request.form["email"]
        print name
        passwd = request.form["password"]
        #validate
        print "run ito login part!"
        user = db.user
        u = db.user.find_one({"_id":name})
        if u:
            if u["password"] == passwd:
                session["uid"]=name       
                print session["uid"]
                return redirect(url_for('firstpage'))     
            else:
                pass
        else:
            pass
                
    return render_template("login.html")
@app.route('/firstpage',methods=['POST','GET'])
def firstpage():
    return render_template('firstpage.html')


@app.route('/personinfo',methods=['POST','GET'])
def personinfo():
    return render_template('personinfo.html')



@app.route('/taskdetail')
def taskdetail():
    return render_template("task_detail.html")

@app.route('/register',methods=['POST','GET'])
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
        

@app.route('/logout')
def logout():
    session['uid'] = None
    return redirect(url_for('login'))
"""

import time
import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback,IOLoop
import tornado.wsgi
import simplejson
from pymongo import Connection

class NowHandler(WebSocketHandler):
    online = {}
    clients=set()
    def on_message(self,message):
        print message
        
        if message!="refresh":
            db = Connection("localhost",27017).nano
            online = db.online
            mlist = message.split(",")
            uid = mlist[0]
            self.userid = mlist[0]
            self.online[self] = uid
            print self.online[self]
            #print "run here@"
            messages = ""
            for m in online.find():
                messages+=m["value"]+";"
            messages=message+";"+messages+";"
            print "run here" 
            if online.find_one({"_id":uid}):
                print "run into find"
                online.update({"_id":uid},{"value":message})
            else:
                online.insert({"_id":uid,"value":message})
            
            self.write_message(messages)
        elif message == "remove":
            print "remove"
        else:
            self.write_message(message)

    def open(self):
        print "run into open"
        NowHandler.clients.add(self)
    
    def on_close(self):
        print "run into close"
        print dir(self.clients)
        print "run into close"
        #print message
        db = Connection("localhost",27017).nano
        online = db.online
        print self.online[self]
        online.remove({"_id":self.online[self]})
        #online.remove({"_id":})
        NowHandler.clients.remove(self)

    #@staticmethod
    #def refresh():
        #NowHandler.on_message("refresh")
        #for client in NowHandler.clients:
        #   client.write_message("refresh")
    #def post(self):
    #    self.scheduler = PeriodicCallback(self.on_message,1000)
    #    self.scheduler.start()

wsgi_app=tornado.wsgi.WSGIContainer(app)

application=tornado.web.Application([
    (r'/now',NowHandler),
    (r'.*',tornado.web.FallbackHandler,{'fallback':wsgi_app })
])

#PeriodicCallback(NowHandler.refresh,20000).start()

print app.url_map
application.listen(5000)
IOLoop.instance().start()

