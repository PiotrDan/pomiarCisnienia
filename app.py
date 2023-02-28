from flask import Flask, render_template, url_for, flash, request, redirect, g
import sqlite3
from datetime import datetime, date

app = Flask(__name__)

app_info = {'db_file':'C:/Users/Szef/Documents/JAVA/Python_Flask/Pomiar ciśnienia/data/blood_diary.db'}

if app.config['ENV'] =='production':
  app.config.from_object('config.ProductionConfig')
elif app.config['ENV'] == 'development':
  app.config.from_object('config.DevelopmentConfig')
else:
  app.config.from_object('config.TestingConfig')   

def get_db():
  if not hasattr(g, 'sqlite_db'):
    conn = sqlite3.connect(app_info['db_file'])
    conn.row_factory = sqlite3.Row
    g.sqlite_db = conn
  return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()       

@app.route('/')
def index():
  db = get_db()
  sql_command = 'select id, upper_pressure, down_pressure, pressure, date_of_pressure from blood_pressure order by date_of_pressure;'
  cur = db.execute(sql_command)
  bloods = cur.fetchall()
  return render_template('index.html', active_menu='home', bloods=bloods)

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

    db = get_db()
    sql_command = 'insert into blood_pressure(upper_pressure, down_pressure, pressure, date_of_pressure, description) values(?, ?, ?, ?, ?);' 
    db.execute(sql_command, [upper_pressure, down_pressure, pressure, date_of_pressure, description])
    db.commit() 

    return render_template('cisnienie_result.html', upper_pressure=upper_pressure,  down_pressure=down_pressure, pressure=pressure, date_of_pressure=date_of_pressure, time_of_day=time_of_day, description=description)  

@app.route('/pressure_history')
def pressure_history():
  db = get_db()
  sql_command = 'select id, upper_pressure, down_pressure, pressure, date_of_pressure, date_of_pressure, time_of_day, description from blood_pressure order by date_of_pressure;'
  cur = db.execute(sql_command)
  bloods = cur.fetchall()
  return render_template('cisnienie.html', active_menu='pressure_history', bloods=bloods)

@app.route('/delete_pressure/<int:pressure_id>')
def delete_pressure(pressure_id):
  db = get_db()
  sql_statment = 'delete from blood_pressure where id=?;'
  db.execute(sql_statment, [pressure_id])
  db.commit()
  return redirect(url_for('pressure_history'))          

@app.route('/edit_pressure/<int:pressure_id>', methods=['GET', 'POST'])
def edit_pressure(pressure_id):  

  
  db = get_db()

  if request.method == 'GET':

    sql_statment = 'select id, upper_pressure, down_pressure, pressure, date_of_pressure, description from blood_pressure where id=?;'
    cur = db.execute(sql_statment, [pressure_id])
    notif_obj = cur.fetchone()

    if notif_obj == None:
      return redirect(url_for('pressure_history'))
    else:
      return render_template('edit_pressure.html', active_menu='history', notif_obj=notif_obj)  

    
  else:
    upper_pressure = 120
    if 'upper_pressure' in request.form:
      upper_pressure = request.form['upper_pressure']

    down_pressure = 80
    if "down_pressure" in request.form:
      down_pressure = request.form['down_pressure']

    pressure = 65
    if "pressure" in request.form:
      pressure = request.form['pressure']    

    date_of_pressure = ''
    if 'date_of_pressure' in request.form:
      date_of_pressure = request.form['date_of_pressure']  

    time_of_day = 'rano'
    if 'time_of_pressure' in request.form:
      time_of_day = request.form['time_of_day']

    description = ''
    if 'description' in request.form:
      description = request.form['description'] 

    sql_command = '''update blood_pressure set
                  upper_pressure = ?,
                  down_pressure = ?,
                  pressure = ?,
                  date_of_pressure = ?,
                  description = ?
                where id = ?    
    '''  
    db.execute(sql_command, [upper_pressure, down_pressure, pressure, date_of_pressure, description, pressure_id])
    db.commit()
    # flash("Dane zostały uaktualnione")
    return redirect(url_for('pressure_history'))

@app.route('/weight_meassure', methods=['GET', 'POST'])
def weight_meassure():

  if request.method == 'GET':
    return render_template('base.html')
  else:
    
    weight = 80
    if 'weight' in request.form:
      weight = int(request.form['weight'])  

    date_of_weight = ''
    if 'date_of_weight' in request.form:
      date_of_weight = request.form['date_of_weight']

    time_of_day = 'rano'
    if 'time_of_day' in request.form:
      time_of_day = request.form['time_of_day']  

    comments = 'brak'
    if 'comments' in request.form:
      comments = request.form['comments']


    db = get_db()
    sql_command = 'INSERT INTO weights (weight, date_of_weight, time_of_day, comments) VALUES (?, ?, ?, ?);'
    db.execute(sql_command, [weight, date_of_weight, time_of_day, comments])
    db.commit()  

  return render_template('weight_result.html', weight=weight, date_of_weight=date_of_weight, time_of_day=time_of_day, comments=comments)    

@app.route('/weight_history')   
def weight_history():
  db = get_db()
  sql_command = 'SELECT id, weight, date_of_weight, comments, round((weight/(1.8*1.8)),2) AS BMI FROM weights;'
  cur = db.execute(sql_command)
  weights = cur.fetchall()
  db.commit()
  return render_template('waga.html', active_menu='weight_history', weights=weights)  

@app.route('/delete_weight/<int:weight_id>')
def delete_weight(weight_id):
  db = get_db()
  sql_statment = 'DELETE FROM weights WHERE id=?;'
  db.execute(sql_statment, [weight_id])
  db.commit()

  return redirect(url_for('weight_history'))






