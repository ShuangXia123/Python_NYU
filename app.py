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
# Find home page
@app.route('/')
def trade_main():
    connection=get_connection()
    sql=('select remain_capital from trade_user')
    result=connection.cmd_query(sql)
    update_capital=connection.get_rows()
    update_capital=float(update_capital[0][0][0])
    update_capital =  round(update_capital,2)
    inv1,inv2,inv3 = get_inventory()
    
            
        
    return render_template('home.html',blc=update_capital,btc=inv1,eth=inv2,ltc=inv3)
# Find trade history
@app.route('/trade_history')
def trade_history():
    inv1,inv2,inv3 = get_inventory()
    rpl1,rpl2,rpl3=get_rpl()
    upl1,upl2,upl3=get_upl()
    return render_template('trade history.html',btc1=inv1,eth1=inv2,ltc1=inv3,
    btc3=rpl1,eth3=rpl2,ltc3=rpl3,btc4=upl1,eth4=upl2,ltc4=upl3)
    # Find btc buy
@app.route('/btc_buy_page')
def buy_bitcoin_buy_page():
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'BTC-USD')
    buy_price = float(buy_info["amount"])
    return render_template('Trading Processing1.html',price = buy_price)
# Find btc sell
@app.route('/btc_sell_page')
def buy_bitcoin_sell_page():
    client = Client('fakeapikey', 'fakeapisecret')
    sell_info = client.get_sell_price(currency_pair = 'BTC-USD')
    sell_price = float(sell_info["amount"])
    return render_template('Trading Processing2.html',price = sell_price)

# Find ETH buy
@app.route('/eth_buy_page')
def buy_ethereum_buy_page():
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'ETH-USD')
    buy_price = float(buy_info["amount"])
    return render_template('Trading Processing3.html',price = buy_price)
# Find ETH sell
@app.route('/eth_sell_page')
def buy_ethereum_sell_page():
    client = Client('fakeapikey', 'fakeapisecret')
    sell_info = client.get_sell_price(currency_pair = 'ETH-USD')
    sell_price = float(sell_info["amount"])
    return render_template('Trading Processing4.html',price = sell_price)

# Find LITE buy
@app.route('/lite_buy_page')
def buy_litecoin_buy_page():
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'LTC-USD')
    buy_price = float(buy_info["amount"])
    return render_template('Trading Processing5.html',price = buy_price)
# Find LITE sell
@app.route('/lite_sell_page')
def buy_litecoin_sell_page():
    client = Client('fakeapikey', 'fakeapisecret')
    sell_info = client.get_sell_price(currency_pair = 'LTC-USD')
    sell_price = float(sell_info["amount"])
    return render_template('Trading Processing6.html',price = sell_price)
    
    
# Process BTC buy
@app.route('/btc_buy', methods=['post'])
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

        inv1,inv2,inv3=get_inventory()
        connection = get_connection() 
        inv1=float(inv1)
        sum_quantity = inv1+qty_float

        avg_price=total_value/inv1
        buy_price=float(buy_price)
        buy_upl=(buy_price-avg_price)*inv1 
        buy_upl=str(buy_upl) 

        buy_price = str(buy_price)
        
        
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
        connection.commit()
        connection.close()
        return render_template('trade buy successfully.html') 
    else: 
        return render_template('trade buy failed transaction.html') 
    
# Process BTC sell
@app.route('/btc_sell', methods=['post'])
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
    
    remain_qty,inv2,inv3=get_inventory()
    remain_qty=float(remain_qty)
    connection = get_connection() 
    if qty_float <= remain_qty:
        sql2=('select sum(item_value) from trade_record where item_id=1')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])
        sql3=('select sum(quantity) from trade_record where item_id=1 and side_id=2')
        result=connection.cmd_query(sql3)
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
        return render_template('trade buy successfully.html') 
    else: 
        return render_template('trade buy failed transaction.html') 

# Process ETH buy
@app.route('/eth_buy', methods=['post'])
def buy_ethereum():
    connection = get_connection() 
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'ETH-USD')
    buy_price = float(buy_info["amount"])
    qty = request.form['qty']
    cmd = connection.cursor()
    cmd.execute("select remain_capital from trade_user where user_id = 1")
    remain = cmd.fetchmany(1)
    remain=float(remain[0][0])
    qty_float = float(qty)
    total_price = qty_float * buy_price
    if total_price<=remain:
        sql2=('select sum(item_value) from trade_record where item_id=2')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])

        inv1,inv2,inv3=get_inventory()
        connection = get_connection() 
        inv2=float(inv2)
        sum_quantity = inv2+qty_float
        avg_price=total_value/inv2
        buy_price=float(buy_price)
        buy_upl=(avg_price-buy_price)*inv2
        buy_upl=str(buy_upl) 

        buy_price = str(buy_price)
        
        
        sum_quantity=str(sum_quantity)
        remain = remain - total_price
        total_price = str(total_price)
        sql = 'insert into trade_record (side_id,item_value,quantity,item_id,price,inventory,RPL,UPL) values (1,'+total_price+','+qty+',2,'+buy_price+','+sum_quantity+',0,'+buy_upl+')'
        result=connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price
        remain = str(remain)
        # update the reamin value to the MySQL database
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)       
        connection.commit()
        connection.close()
        return render_template('trade buy successfully.html') 
    else: 
        return render_template('trade buy failed transaction.html') 
    

@app.route('/eth_sell', methods=['post'])
def sell_ethereum():
    connection = get_connection() 
    client = Client('fakeapikey', 'fakeapisecret')
    sell_info = client.get_sell_price(currency_pair = 'ETH-USD')
    sell_price = float(sell_info["amount"])
    qty = request.form['qty']
    cmd = connection.cursor()
    cmd.execute("select remain_capital from trade_user where user_id = 1")
    remain = cmd.fetchmany(1)
    remain=float(remain[0][0])
    qty_float = float(qty)
    total_price = qty_float * sell_price
    inv1,remain_qty,inv3=get_inventory()
    remain_qty=float(remain_qty)
    connection = get_connection() 

    if qty_float <= remain_qty:
        sql2=('select sum(item_value) from trade_record where item_id=2')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])
        sql3=('select sum(quantity) from trade_record where item_id=2 and side_id=2')
        result=connection.cmd_query(sql3)
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
        sql = 'insert into trade_record (side_id,item_value,quantity,item_id,price,inventory,UPL,RPL) values (2,'+total_price+','+qty+',2,'+sell_price+','+remain_qty+','+sell_upl+','+sell_rpl+')'
        result = connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price
        #remain = remain + total_price
        #remain_qty = remain_qty - qty_float
        remain = str(remain)
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)
        connection.commit()
        connection.close()
        return render_template('trade buy successfully.html') 
    else: 
        return render_template('trade buy failed transaction.html') 

@app.route('/ltc_buy', methods=['post'])
def buy_litecoin():
    connection = get_connection() 
    client = Client('fakeapikey', 'fakeapisecret')
    buy_info = client.get_buy_price(currency_pair = 'LTC-USD')
    buy_price = float(buy_info["amount"])
    qty = request.form['qty']
    cmd = connection.cursor()
    cmd.execute("select remain_capital from trade_user where user_id = 1")
    remain = cmd.fetchmany(1)
    remain=float(remain[0][0])
    qty_float = float(qty)
    total_price = qty_float * buy_price
    if total_price<=remain:
        sql2=('select sum(item_value) from trade_record where item_id=3')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])
        inv1,inv2,inv3=get_inventory()
        connection = get_connection() 
        inv3=float(inv3)
        sum_quantity = inv3+qty_float

        

        avg_price=total_value/inv3
        buy_price=float(buy_price)
        buy_upl=(avg_price-buy_price)*inv3
        buy_upl=str(buy_upl) 

        buy_price = str(buy_price)
        
        sum_quantity=str(sum_quantity)
        remain = remain - total_price
        total_price = str(total_price)
        sql = 'insert into trade_record (side_id,item_value,quantity,item_id,price,inventory,RPL,UPL) values (1,'+total_price+','+qty+',3,'+buy_price+','+sum_quantity+',0,'+buy_upl+')'
        result=connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price
        remain = str(remain)
        # update the reamin value to the MySQL database
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)       
        connection.commit()
        connection.close()
        return render_template('trade buy successfully.html') 
    else: 
        return render_template('trade buy failed transaction.html') 
    

@app.route('/ltc_sell', methods=['post'])
def sell_litecoin():
    connection = get_connection() 
    client = Client('fakeapikey', 'fakeapisecret')
    sell_info = client.get_sell_price(currency_pair = 'LTC-USD')
    sell_price = float(sell_info["amount"])
    qty = request.form['qty']
    cmd = connection.cursor()
    cmd.execute("select remain_capital from trade_user where user_id = 1")
    remain = cmd.fetchmany(1)
    remain=float(remain[0][0])
    qty_float = float(qty)
    total_price = qty_float * sell_price
    inv1,inv2,remain_qty=get_inventory()
    remain_qty=float(remain_qty)
    connection = get_connection() 
    if qty_float <= remain_qty:
        sql2=('select sum(item_value) from trade_record where item_id=3')
        result=connection.cmd_query(sql2)
        total_value=connection.get_rows()
        total_value=float(total_value[0][0][0])
        sql3=('select sum(quantity) from trade_record where item_id=3 and side_id=2')
        result=connection.cmd_query(sql3)
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
        sql = 'insert into trade_record (side_id,item_value,quantity,item_id,price,inventory,UPL,RPL) values (2,'+total_price+','+qty+',3,'+sell_price+','+remain_qty+','+sell_upl+','+sell_rpl+')'
        result = connection.cmd_query(sql)
        # insert the price to the database, the variable of price is buy_price
        #remain = remain + total_price
        #remain_qty = remain_qty - qty_float
        remain = str(remain)
        sql1='update trade_user set remain_capital='+remain+' where user_id=1'
        result=connection.cmd_query(sql1)
        connection.commit()
        connection.close()
        return render_template('trade buy successfully.html') 
    else: 
        return render_template('trade buy failed transaction.html') 


def get_inventory():
    connection=get_connection()
    sql1=('select inventory from trade_record where item_id=1 order by trade_id desc limit 1')
    result=connection.cmd_query(sql1)
    update_inventory1=connection.get_rows()
    update_inventory1=str(update_inventory1[0][0][0])
    sql2=('select inventory from trade_record where item_id=2 order by trade_id desc limit 1')
    result=connection.cmd_query(sql2)
    update_inventory2=connection.get_rows()
    update_inventory2=str(update_inventory2[0][0][0])
    sql3=('select inventory from trade_record where item_id=3 order by trade_id desc limit 1')
    result=connection.cmd_query(sql3)
    update_inventory3=connection.get_rows()
    update_inventory3=str(update_inventory3[0][0][0])
    return update_inventory1, update_inventory2,update_inventory3
    connection.commit()
    connection.close()


@app.route('/graph1')
def graph1():
    pl = [[1,0],[2,0],[3,-61229],[4,0],[5,-323308]]
    return render_template('graph1.html',pl1=pl) 


def get_rpl():
    connection=get_connection()
    sql=('select sum(RPL) from trade_record where item_id=1')
    result=connection.cmd_query(sql)
    update_rpl1=connection.get_rows()
    update_rpl1=float(update_rpl1[0][0][0])
    update_rpl1=round(update_rpl1, 2)
    sql2=('select sum(RPL) from trade_record where item_id=2')
    result=connection.cmd_query(sql2)
    update_rpl2=connection.get_rows()
    update_rpl2=float(update_rpl2[0][0][0])
    update_rpl2=round(update_rpl2, 2)
    sql3=('select sum(RPL) from trade_record where item_id=3')
    result=connection.cmd_query(sql3)
    update_rpl3=connection.get_rows()
    update_rpl3=float(update_rpl3[0][0][0])
    update_rpl3=round(update_rpl3, 2)
    return update_rpl1, update_rpl2, update_rpl3
    connection.commit()
    connection.close()

def get_upl():
    connection=get_connection()
    sql=('select UPL from trade_record where item_id=1')
    result=connection.cmd_query(sql)
    update_upl1=connection.get_rows()
    update_upl1=float(update_upl1[0][0][0])
    update_upl1=round(update_upl1, 2)
    sql2=('select UPL from trade_record where item_id=2')
    result=connection.cmd_query(sql2)
    update_upl2=connection.get_rows()
    update_upl2=float(update_upl2[0][0][0])
    update_upl2=round(update_upl2, 2)

    sql3=('select UPL from trade_record where item_id=3')
    result=connection.cmd_query(sql3)
    update_upl3=connection.get_rows()
    update_upl3=float(update_upl3[0][0][0])
    update_upl3=round(update_upl3, 2)
    return update_upl1, update_upl2, update_upl3
    connection.commit()
    connection.close()

