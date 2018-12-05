
from flask import Flask
from flask import request
from flask import render_template
import mysql.connector as mc
app=Flask(__name__)
def get_connection():
    return mc.connect(user='root',
    password='xia19940124',
    host='127.0.0.1',
    database='trade_system',
    auth_plugin='mysql_native_password')

def get_products():
    connection=get_connection()
    result=connection.cmd_query("select * from trade_items")
    rows=connection.get_rows()
    connection.close()
    return rows[0]

@app.route('/')
def trade_main():
    products=get_products()
    return render_template('trade_main.html',products=products)
