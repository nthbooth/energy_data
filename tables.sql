use power
create table smartmeter_consumption(
electricity double default NULL,
electricity_production double default NULL,
gas_kwh double default NULL,
gas double default NULL,
timestamp DATETIME NOT NULL PRIMARY KEY, 
UNIQUE (timestamp)
);


create table power_data(
electricity double default NULL,
electricity_production double default NULL,
gas_kwh double default NULL,
gas double default NULL,
solar_generation double default NULL,
timestamp DATETIME NOT NULL PRIMARY KEY,
UNIQUE (timestamp)
);


create unique index index_smartmeter_consumption on smartmeter_consumption (timestamp);

create table smartmeter_last_timestamps(
metric varchar(30) not null PRIMARY KEY,
timestamp DATETIME not null
);

create table solaredge(
electricity_production double default NULL,
timestamp DATETIME NOT NULL PRIMARY KEY, 
UNIQUE (timestamp)
);

create unique index index_solaredge on solaredge (timestamp);

create table solaredge_last_timestamps(
metric varchar(30) not null PRIMARY KEY,
timestamp DATETIME not null
);

