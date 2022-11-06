#queries for the one pager:

select 
case 	when reply_date between '2021-01-01' and '2021-03-31' then '21-q1'
        when reply_date between '2021-04-01' and '2021-06-30' then '21-q2'
        when reply_date between '2021-07-01' and '2021-09-30' then '21-q3'
		when reply_date between '2021-10-01' and '2021-12-31' then '21-q4' 
        when reply_date between '2022-01-01' and '2022-03-31' then '22-q1'
        when reply_date between '2022-04-01' and '2022-06-30' then '22-q2'
end as Q
,iec_reply_code
,count(id) as num_of_requests
,sum(requested_power) as sum_of_requested_power
from reply_from_iec_inc_enum as a
#where reg_code not in (280, 290) /*gas regulations*/  
group by Q, iec_reply_code
order by Q, iec_reply_code;


# wind regulations: 905, 935
# gas regulations: 280, 290
select 		
req_power_segments		
,sum(requested_power) as total_requested_power_kw		
,count(id) as num_of_requests		
from (		
	select 	
	a.*	
	,case when requested_power<=15 then '0-15'	
		when requested_power between 16 and 100 then '016-100'
		when requested_power between 101 and 200 then '101-200'
		when requested_power between 201 and 300 then '201-300'
		when requested_power between 301 and 400 then '301-400'
		when requested_power between 401 and 500 then '401-500'
		when requested_power between 501 and 630 then '501-630'
        when requested_power between 631 and 2000 then '630-2000'		
		when requested_power>2000 then 'higher_than_2000'
		end as req_power_segments
	from reply_from_iec_inc_enum as a	
    where reg_code not in (280, 290, 905, 935) and reply_date>='2022-01-01'		
) as sub		
group by req_power_segments		
order by req_power_segments;		



### only taarifiot
select 		
req_power_segments		
,sum(requested_power) as total_requested_power_kw		
,count(id) as num_of_requests		
from (		
	select 	
	a.*	
	,case when requested_power<=15 then '0-15'	
		when requested_power between 16 and 100 then '016-100'
		when requested_power between 101 and 200 then '101-200'
		when requested_power between 201 and 300 then '201-300'
		when requested_power between 301 and 400 then '301-400'
		when requested_power between 401 and 500 then '401-500'
		when requested_power between 501 and 630 then '501-630'
        when requested_power between 631 and 2000 then '630-2000'		
		when requested_power>2000 then 'higher_than_2000'
		end as req_power_segments
	from reply_from_iec_inc_enum as a		
	where reply_date>='2022-01-01' and reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313, 350, 351, 352)
) as sub		
group by req_power_segments		
order by req_power_segments		


select reg_code, count(*) as c
from reply_from_iec_inc_enum
group by reg_code
order by c

##### connection to the grid ############

select
napa_code,
sum(requested_power_dc)*1.0/1000 as sum_requested_power_dc
from (
select
napa_code,
reg_code,
case 	when reg_code in (133, 134, 161) then requested_power*1.3 /*ground*/
		when reg_code in (140, 141, 142, 160, 250, 300, 301, 305, 308, 310, 311, 312, 350, 378, 941, 942, 946, 964, 969) then requested_power*1.2 /*dual use*/
        when reg_code in (905) then requested_power /*wind*/
end as requested_power_dc
from connection_to_the_grid_enum
where reg_code not in (280, 290) ## without gas reg.
and operation_start_date>='2022-01-01'
) as sub
group by 1
order by 1

select sum(requested_power)
from connection_to_the_grid_enum
where reg_code not in (905, 935, 280, 290) 
and operation_start_date>='2022-01-01'


select reg_code, count(*), sum(requested_power)
from connection_to_the_grid_enum
where reg_code not in (280, 290)  and operation_start_date>='2022-01-01'
group by reg_code




##################  SANITY CHECKS ####################################
drop table reply_from_iec_inc_enum_temp #tshuvat_mechalek_q1_2022.txt
CREATE TABLE reply_from_iec_inc_enum_temp (
            id INT NOT NULL AUTO_INCREMENT,
            agaf_code INT NOT NULL,
            napa_code INT NOT NULL,
            yishuv_code INT NOT NULL,
            reg_code INT NOT NULL,
            requested_power INT NOT NULL,
            voltage_code INT NOT NULL,
            iec_reply_code INT NOT NULL,
            reply_date date NOT NULL,
            PRIMARY KEY (id)
);

select count(*) from reply_from_iec_inc_enum_temp;
select count(*) from reply_from_iec_inc_enum;

select * from reply_from_iec_inc_enum_temp;

select * from reply_from_iec_inc_enum as a
left join reply_from_iec_inc_enum_temp as b on a.yishuv_code=b.yishuv_code and a.requested_power=b.requested_power and a.iec_reply_code=b.iec_reply_code and 
	a.reply_date=b.reply_date and a.reg_code=b.reg_code
where a.reply_date between '2022-01-01' and '2022-03-31'
and b.id is null;


select iec_reply_code, sum(requested_power)
from reply_from_iec_inc_enum
where reply_date<'2022-01-01'
group by iec_reply_code



select * from reply_from_iec_inc_enum as a
where a.reply_date between '2022-01-01' and '2022-03-31'
and yishuv_code=305;


select max(operation_start_date) from connection_to_the_grid_enum

drop table connection_to_the_grid_enum_temp;
CREATE TABLE connection_to_the_grid_enum_temp (
            id INT NOT NULL AUTO_INCREMENT,
            agaf_code INT NOT NULL,
            napa_code INT NOT NULL,
            yishuv_code INT NOT NULL,
            reg_code INT NOT NULL,
            requested_power INT NOT NULL,
            voltage_code INT NOT NULL,
            operation_start_date date NOT NULL,
            PRIMARY KEY (id)
);

select count(*) from connection_to_the_grid_enum_temp; #2424
select count(*) from connection_to_the_grid_enum where operation_start_date between '2022-01-01' and '2022-03-31'; #2412

select * from connection_to_the_grid_enum_temp as a
left join connection_to_the_grid_enum as b on a.yishuv_code=b.yishuv_code and a.requested_power=b.requested_power and a.operation_start_date=b.operation_start_date 
	and a.reg_code=b.reg_code  
where b.id is null;

select * from connection_to_the_grid_enum 
where yishuv_code = 1206 and reg_code=312 


and operation_start_date='2022-01-24'
