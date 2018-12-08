from flask import Flask
from flask import request
from flask import render_template
import mysql.connector as mc
from coinbase.wallet.client import Client
#$env:FLASK_DEBUG=1
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
    return render_template('home.html',products=products)

@app.route('/btc_page', methods=['post'])


def buy_bitcoin_page():
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'BTC-USD')
    buy_price = float(buy_info["amount"])
    return render_template('Trading Processing1.html', price = buy_price) 
    

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
        sql2=('select sum(item_value) from trade_record where item_id=1')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])

        sql3=('select sum(quantity) from trade_record where side_id=1')
        result=connection.cmd_query(sql3)
        total_quantity=connection.get_rows()
        total_quantity=int(total_quantity[0][0][0])

        avg_price=total_value/total_quantity
        buy_price=float(buy_price)
        buy_upl=(avg_price-buy_price)*total_quantity 
        buy_upl=str(buy_upl) 

        buy_price = str(buy_price)
        sql=("select sum(quantity) from trade_record where item_id=1")
        result=connection.cmd_query(sql)
        sum_quantity=connection.get_rows()
        sum_quantity=int(sum_quantity[0][0][0])+qty_float
        sum_quantity=str(sum_quantity)
        remain = remain - total_price
        total_price = str(total_price)
        sql = 'insert into trade_record (side_id,item_value,quantity,item_id,price,inventory,RPL,UPL) values (1,'+total_price+','+qty+',1,'+buy_price+','+sum_quantity+',0,'+buy_upl+')'
        result=connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price

       
        remain = str(remain)
        # update the reamin value to the MySQL database
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)

        pl = [[2000,11920],[2001,13170],[2002,14550],[2003,11920],[2004,13170],[2005,14550]]
       
               
        connection.commit()
        connection.close()
        return render_template('graph.html', pl1 = pl) 
        # pl = [[2000,11920],[2001,13170],[2002,14550]]
    else: 
        return "有内鬼!" ''
    

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
        sql2=('select sum(item_value) from trade_record where item_id=1')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])
        sql3=('select sum(quantity) from trade_record where item_id=1 and side_id=1')
        result=connection.cmd_query(sql2)
        total_quantity=connection.get_rows()
        total_quantity=int(total_quantity[0][0][0])

        avg_price=total_value/total_quantity

        sell_rpl=(sell_price-avg_price)*qty_float
        
        
        remain = remain + total_price
        total_price=str(total_price)
        remain_qty = remain_qty - qty_float
        sell_upl=(sell_price-avg_price)*remain_qty
        remain_qty=str(remain_qty)
        sell_price = str(sell_price)
        sell_upl=str(sell_upl)
        sell_rpl=str(sell_rpl)
        sql = 'insert into trade_record (side_id,item_value,quantity,item_id,price,inventory,UPL,RPL) values (2,'+total_price+','+qty+',1,'+sell_price+','+remain_qty+','+sell_upl+','+sell_rpl+')'
        result = connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price

        #remain = remain + total_price
        #remain_qty = remain_qty - qty_float
        remain = str(remain)
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)


        connection.commit()
        connection.close()
        return "Order process!"
    else: 
        return "有内鬼!"

def add_inventory(qty_input,buy_price_input):
    qty=qty_input
    buy_price=buy_price_input
    connection=get_connection()
    sql=("select sum(quantity) from trade_record where item_id=1")
    result=connection.cmd_query(sql)
    sum_quantity=connection.get_rows()
    sum_quantity=int(sum_quantity[0][0][0])+qty
    sum_quantity=str(sum_quantity)
    sql2 = 'insert into trade_record (quantity,item_id,price,inventory) values ('+qty+',1,'+buy_price+','+sum_quantity+')'
    result=connection.cmd_query(sql2)
    connection.commit()
    connection.close()
