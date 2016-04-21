import datetime
from flask import url_for
from __init__ import db 

class Data(db.Document):
  domain = db.StringField()
  address = db.StringField()
  property = db.StringField()
  timestamp = db.DateTimeField(unique=True)
  value = db.IntField()
    
  def get_absolute_url(self):
    return url_for('post', kwargs={"slug": self.slug})

  def __unicode__(self):
    return self.address

class PiInfo(db.Document):
  ip = db.StringField()
  mac = db.StringField()
  description = db.StringField()
  alias = db.StringField()

  def get_absoluter_url(self):
    return url_for('post', kwargs={"slug": self.slug})

  def __unicode__(self):
    return self.ip
