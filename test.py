from flask import Flask
from flask import request
from flask import render_template
import mysql.connector as mc
from coinbase.wallet.client import Client





def get_connection():
    return mc.connect(user='root',
    password='lihenan123',
    host='127.0.0.1',
    database='trade_system',
    auth_plugin='mysql_native_password')
connection = get_connection()
sql=("select RPL from trade_record where item_id = 1")
cmd = connection.cursor()
result=connection.cmd_query(sql)
value=connection.get_rows()
value=float(value[0][2][0])
print(value)
sql1=("select trade_id from trade_record order by trade_id desc limit 1")
result=connection.cmd_query(sql1)
lengh=connection.get_rows()
lengh=int(lengh[0][0][0])
pl=[]
for i in range(0,lengh-1):
    value=float(value[0][i][0])
    pl.append([i,value])
print(pl)
