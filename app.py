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

@app.route('/blood_presure', methods=['POST', 'GET'])
def blood_presure():

  if request.method == 'GET':
    return render_template('base.html')
  else:
    
    upper_pressure = 120
    if 'upper_pressure' in request.form:
      upper_pressure = int(request.form['upper_pressure'])

    down_pressure = 80
    if 'down_pressure' in request.form:
      down_pressure = int(request.form['down_pressure'])

    pressure = 20
    if 'pressure' in request.form:
      pressure = int(request.form['pressure'])

    date_of_pressure = ''
    if 'date_of_pressure' in request.form:
      date_of_pressure = request.form['date_of_pressure']  

    time_of_day = 'rano'
    if 'time_of_pressure' in request.form:
      time_of_day = request.form['time_of_day']

    description = ''
    if 'description' in request.form:
      description = request.form['description']  

    return render_template('cisnienie_result.html', upper_pressure=upper_pressure,  down_pressure=down_pressure, pressure=pressure, date_of_pressure=date_of_pressure, time_of_day=time_of_day, description=description)    







