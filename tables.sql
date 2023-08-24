use power
create table smartmeter_consumption(
electricity double default NULL,
electricity_production double default NULL,
gas_kwh double default NULL,
gas double default NULL,
timestamp DATETIME NOT NULL, 
UNIQUE (timestamp)
);


create unique index index_smartmeter_consumption on smartmeter_consumption (timestamp);

create table smartmeter_last_timestamps(
metric varchar(30) not null,
timestamp DATETIME not null
);

