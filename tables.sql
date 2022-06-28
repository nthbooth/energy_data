
create table smartmeter_consumption(
electricity float default NULL,
gas float default NULL
timestamp DATETIME NOT NULL, 
UNIQUE (timestamp)
);


#alter table smartmeter_consumption add column gas float;
#alter table smartmeter_consumption modify energy_this_period float default NULL;
#alter table smartmeter_consumption change energy_this_period electricity float;
create unique index index_smartmeter_consumption on smartmeter_consumption (timestamp);

create table smartmeter_last_timestamps(
metric varchar(12) not null,
timestamp DATETIME not null
);

