USE `nzo_db`;

DROP TABLE noga_expost_data_raw;
CREATE TABLE noga_expost_data_raw (
            id INT NOT NULL AUTO_INCREMENT,
            rec_date date NOT NULL,
            rec_time time NOT NULL,
            cost double NOT NULL,
            renewable_gen double NOT NULL,
            conventional_gen double NOT NULL,
            system_demand double NOT NULL,
            PRIMARY KEY (id)
);

select max(rec_date) from noga_expost_data_raw
describe noga_expost_data_raw

select max(rec_date) from noga_expost_data_raw

select * from noga_expost_data_raw where rec_date >= '2022-07-01'

select 
rec_year,
rec_month,
sum(renewable_gen_hourly) as renewable_gen_hourly_sum,
sum(conventional_gen_hourly) as conventional_gen_hourly_sum,
sum(system_demand_hourly) as system_demand_hourly_sum
from (
select 
rec_date,
year(rec_date) as rec_year,
month(rec_date) as rec_month,
rec_time,
cost,
renewable_gen,
renewable_gen*0.5+ (LAG(renewable_gen) over (order by id))*0.5 as renewable_gen_hourly,
conventional_gen,
conventional_gen*0.5+ (LAG(conventional_gen) over (order by id))*0.5 as conventional_gen_hourly,
system_demand,
system_demand*0.5+ (LAG(system_demand) over (order by id))*0.5 as system_demand_hourly
from noga_expost_data_raw
order by id
) as sub
where rec_time like "%:30:%"
group by rec_year, rec_month


select 
rec_year,
rec_month,
rec_day,
sum(renewable_gen_hourly) as renewable_gen_hourly_sum,
sum(conventional_gen_hourly) as conventional_gen_hourly_sum,
sum(system_demand_hourly) as system_demand_hourly_sum,
max(renewable_gen_hourly) as max_hourly_renewable_gen,
max(renewable_gen_hourly*1.0/system_demand_hourly) as max_pcg_hourly_renewable_gen
from (
select 
rec_date,
day(rec_date) as rec_day,
year(rec_date) as rec_year,
month(rec_date) as rec_month,
rec_time,
cost,
renewable_gen,
renewable_gen*0.5+ (LAG(renewable_gen) over (order by id))*0.5 as renewable_gen_hourly,
conventional_gen,
conventional_gen*0.5+ (LAG(conventional_gen) over (order by id))*0.5 as conventional_gen_hourly,
system_demand,
system_demand*0.5+ (LAG(system_demand) over (order by id))*0.5 as system_demand_hourly
from noga_expost_data_raw
order by id
) as sub
where rec_time like "%:30:%" and rec_year='2022'
group by rec_year, rec_month, rec_day


select 
max(renewable_gen_hourly) as max_renewable_gen_hourly,
max(renewable_gen_hourly*1.0/system_demand_hourly) as max_pcg_hourly_renewable_gen
from (
select 
rec_date,
day(rec_date) as rec_day,
year(rec_date) as rec_year,
month(rec_date) as rec_month,
rec_time,
cost,
renewable_gen,
renewable_gen*0.5+ (LAG(renewable_gen) over (order by id))*0.5 as renewable_gen_hourly,
conventional_gen,
conventional_gen*0.5+ (LAG(conventional_gen) over (order by id))*0.5 as conventional_gen_hourly,
system_demand,
system_demand*0.5+ (LAG(system_demand) over (order by id))*0.5 as system_demand_hourly
from noga_expost_data_raw
order by id
) as sub
where rec_time like "%:30:%" and rec_year='2022' 


select 
*
from (
select 
rec_date,
day(rec_date) as rec_day,
year(rec_date) as rec_year,
month(rec_date) as rec_month,
rec_time,
cost,
renewable_gen,
renewable_gen*0.5+ (LAG(renewable_gen) over (order by id))*0.5 as renewable_gen_hourly,
conventional_gen,
conventional_gen*0.5+ (LAG(conventional_gen) over (order by id))*0.5 as conventional_gen_hourly,
system_demand,
system_demand*0.5+ (LAG(system_demand) over (order by id))*0.5 as system_demand_hourly
from noga_expost_data_raw
order by id
) as sub
where renewable_gen_hourly*1.0/system_demand_hourly>0.4 and rec_year='2022' 


select 
year(rec_date) as rec_year,
month(rec_date) as rec_month,
day(rec_date) as rec_day,
count(*) as cnt
from noga_expost_data_raw
where month(rec_date)=5 and year(rec_date)=2022
group by 1, 2, 3

select day(rec_date), count(*)
from noga_expost_data
where  month(rec_date)=3 and year(rec_date)=2022
group by 1