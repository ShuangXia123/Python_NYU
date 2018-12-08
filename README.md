# Python_NYU
create table trade_system;
use table trade_system;
create table trade_record (
trade_id int not null auto_increment,
item_id int,
quantity int,
inventory int,
price varchar(55),
UPL varchar(55),
item_value varchar(55),
side_id int,
RPL varchar(55),
primary key (trade_id)
);
create table side_table (
side_id int not null auto_increment,
side_name varchar(4),
primary key (side_id)
);
create table (
pl_id int not null auto_increment,
item_id int,
inventory int,
avg_price varchar(55),
UPL varchar(55),
RPL varchar(55),
primary key (pl_id)
);
trade_item (
item_id int not null auto_increment,
symbol varchar(10),
item_name varcahr(10),
primary key (item_id)
);
insert into trade_item values (1,'BTC','Bitcoin'),(2,'ETH','Ethereum'),(3,'LTC','Litecoin');
