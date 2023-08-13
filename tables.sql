use power
create table smartmeter_consumption(
electricity float default NULL,
electricity_production float default NULL,
gas float default NULL,
timestamp DATETIME NOT NULL, 
UNIQUE (timestamp)
);


create unique index index_smartmeter_consumption on smartmeter_consumption (timestamp);

create table smartmeter_last_timestamps(
metric varchar(12) not null,
timestamp DATETIME not null
);

