from flask import Flask, render_template, url_for, flash, request, redirect
import sqlite3
from datetime import datetime, date

app = Flask(__name__)

if app.config['ENV'] =='production':
  app.config.from_object('config.ProductionConfig')
elif app.config['ENV'] == 'development':
  app.config.from_object('config.DevelopmentConfig')
else:
  app.config.from_object('config.TestingConfig')    

@app.route('/')
def index():
  return render_template('index.html')

