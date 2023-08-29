use power

create table power_data(
electricity double default NULL,
electricity_export double default NULL,
gas_kwh double default NULL,
gas double default NULL,
solar_generation double default NULL,
timestamp DATETIME NOT NULL PRIMARY KEY,
UNIQUE (timestamp)
);
create unique index index_power_data on power_data (timestamp);

create table timestamps(
metric varchar(30) not null PRIMARY KEY,
timestamp DATETIME not null
);

create table solaredge(
solar_generation double default NULL,
timestamp DATETIME NOT NULL PRIMARY KEY, 
UNIQUE (timestamp)
);

create unique index index_solaredge on solaredge (timestamp);

