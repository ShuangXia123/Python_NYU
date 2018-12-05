from flask import Flask
from flask import request
from flask import render_template
import mysql.connector as mc
from coinbase.wallet.client import Client

app=Flask(__name__)
def get_connection():
    return mc.connect(user='root',
    password='lihenan123',
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

@app.route('/process1', methods=['post'])

def buy_bitcoin():
    connection = get_connection() 
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'BTC-USD')
    buy_price = float(buy_info["amount"])
    qty = request.form['qty']
    cmd = connection.cursor()
    cmd.execute("select remain_capital from trade_user where user_id = 1")
    remain = cmd.fetchmany(1)
    remain=float(remain[0][0])
    qty_float = float(qty)
    total_price = qty_float * buy_price
    if total_price<=remain:
        buy_price = str(buy_price)
        sql = 'insert into trade_record (quantity,item_id,price) values ('+qty+',1,'+buy_price+')'
        result = connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price

        remain = remain - total_price
        remain = str(remain)
        # update the reamin value to the MySQL database
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)


        connection.commit()
        connection.close()
        return render_template('graph.html')
    else: 
        return "有内鬼!"

@app.route('/process2', methods=['post'])
def sell_bitcoin():
    connection = get_connection() 
    client = Client('fakeapikey', 'fakeapisecret')
    sell_info = client.get_sell_price(currency_pair = 'BTC-USD')
    sell_price = float(sell_info["amount"])
    qty = request.form['qty']
    cmd = connection.cursor()
    cmd.execute("select remain_capital from trade_user where user_id = 1")
    remain = cmd.fetchmany(1)
    remain=float(remain[0][0])
    qty_float = float(qty)
    total_price = qty_float * sell_price
    cmd.execute ("select sum(quantity) from trade_record where item_id=1")
    remain_qty=cmd.fetchmany(1)
    remain_qty=int(remain_qty[0][0])

    if qty_float <= remain_qty:
        sell_price = str(sell_price)
        sql = 'insert into trade_record (quantity,item_id,price) values ('+qty+',1,'+sell_price+')'
        result = connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price

        remain = remain - total_price
        remain_qty = remain_qty - qty_float
        remain = str(remain)
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)


        connection.commit()
        connection.close()
        return "Order process!"
    else: 
        return "有内鬼!"
