#!/usr/bin/env python
from flask import Flask, request
from flask import render_template
from flask import Response
from flask import json
from crossdomain import *
import time
import datetime
import flask
from time import mktime
from datetime import datetime

from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from mongoengine import *
from flask.ext.sillywalk import SwaggerApiRegistry, ApiParameter, ApiErrorResponse

from models import *

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {'DB': "ecaldatas"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

@app.route("/")
@crossdomain(origin='*')
def hello():
  address = request.args.get('address', '')
 # domain = request.args.get('domain', '')
 # property = request.args.get('property', '')
  _from = request.args.get('from', '')
  _to = request.args.get('to', '')
      
  if address == '':
    data = Data.objects.all()[:500] # Limit to 500 results if all
  else:
# get the time stuffs
    dt_from = datetime.datetime.strptime(_from, "%d/%m/%Y_%H:%M:%S").timetuple()
    dt_to   = datetime.datetime.strptime(_to, "%d/%m/%Y_%H:%M:%S").timetuple()
    fromtimestamp = datetime.datetime.fromtimestamp(mktime(dt_from))
    totimestamp = datetime.datetime.fromtimestamp(mktime(dt_to))
    #data = Data.objects(( Q(address=address) & Q(timestamp__gt=fromtimestamp) & Q(timestamp__lt=totimestamp) ))
    data = Data.objects(( Q(address=address) & Q(timestamp__gt=fromtimestamp) & Q(timestamp__lt=totimestamp) ))
 # length = str(len(Data.objects))
#  data = Data.objects.all()[:500] 
  js = json.dumps(data)
  resp = Response(js, status=200, mimetype='application/json')
  return resp

@app.route("/live")
@crossdomain(origin='*')
def live():
  limit = int(request.args.get('limit', 30))
  address = request.args.get('address', '')
  data = []
  if address != '':
    data = Data.objects(( Q(address=address) )).order_by('-id').limit(limit)  
  else: 
    data = Data.objects.all().order_by('-id').limit(limit)
  
  js = "hellou"
  try:
    for u in data:
      u.property = "tibor"
    js = json.dumps(data)
#    js = str(type(js))
  except Exception as e:
    js = "the type of u is " + str(type(u))
 # for u in js:
 #   u.property = ''
  
  resp = Response(js, status=200, mimetype='application/json')
  return resp

@app.route("/all")
@crossdomain(origin='*')
def all():
  address = request.args.get('address', '')
  if address != '':
     data = Data.objects(( Q(address=address) )).all().order_by('-timestamp')
  else:
     data = {}   
  js = json.dumps(data)
  resp = Response(js, status=200, mimetype='application/json')
  return resp

@app.route("/infos")
@crossdomain(origin='*')
def infos():
   data = PiInfo.objects.all()
   js = json.dumps(data)
   resp = Response(js, status=200, mimetype='application/json')
   return resp

@app.route("/add", methods=['GET', 'POST'])
def add():
    dtime = datetime.datetime.fromtimestamp(
                                            int(int(request.form["timestamp"])/1000)
                                            )
    d = Data(domain=request.form["domain"], address=request.form["address"], property=request.form["property"], timestamp=dtime, value=request.form["value"])
    d.save()
    return ('', 204)

@app.route("/updatePi", methods=['GET', 'POST'])
def updatePi():
    mac = request.form['mac']
    ip = request.form['ip']
    desc = request.args.get('description', '')

    dict_alias = { "b8:27:eb:fb:53:4b" : "Dark Snowflake", "b8:27:eb:59:c3:ae" : "Shy Waterfall", "b8:27:eb:0d:5f:9c" : "Mighty Savannah", "b8:27:eb:51:c3:5e" : "Delicate River", "b8:27:eb:ae:af:16" : "Mirror Bee", "b8:27:eb:43:ee:83" : "Undefined Peanut", "b8:27:eb:9f:f8:52" : "Broken Moon", "b8:27:eb:2b:80:ee":"Giggling Forest"}
    alias = dict_alias.get(mac, '')
    
    PiInfo.objects(mac=mac).update_one(set__ip = ip, set__description = desc, set__alias=alias, upsert=True)
    return ('', 204)


@app.route("/api")
def apiDoc():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

