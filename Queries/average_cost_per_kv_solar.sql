select reg_code, sum(requested_power)
from connection_to_the_grid_enum as a	
where reg_code not in (280, 290, 905, 935) and operation_start_date>='2022-01-01'	
group by reg_code;



select
sum(requested_power) as total_requested_power
,sum(case when reg_code in (133, 134, 140, 141, 142, 160, 161, 170, 171, 180) or (reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313) and requested_power<=630) then requested_power else 0 end)
	as included_req_power
,sum(cost_per_connection) as sum_cost_per_connection
,sum(case when reg_code not in (133, 134, 140, 141, 142, 160, 161, 170, 171, 180) and not (reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313) and requested_power<=630) then requested_power else 0 end)
	as not_included_req_power
from (
select 
reg_code,
requested_power,
case when reg_code = 130 then 20.38*requested_power
when reg_code = 133 then 18.62*requested_power
when reg_code = 134 then 18.3*requested_power
when reg_code = 140 then 23.77*requested_power
when reg_code = 141 then 23.48*requested_power
when reg_code = 142 then 18.64*requested_power
when reg_code = 160 then 23.01*requested_power
when reg_code = 161 then 17.94*requested_power
when reg_code = 170 then 20.42*requested_power
when reg_code = 171 then 17.87*requested_power
when reg_code = 180 then 17.08*requested_power
when reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313) and requested_power<=15 then 48*requested_power
when reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313) and requested_power<=100 then 48*15+41*(requested_power-15)
when reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313) and requested_power<=300 then 48*15+41*85+24.5*(requested_power-100)
when reg_code in (250, 300, 301, 305, 308, 310, 311, 312, 313) and requested_power<=630 then 48*15+41*85+24.5*200+18.91*(requested_power-300)
else 0 end as cost_per_connection
from connection_to_the_grid_enum as a	
where reg_code not in (280, 290, 905, 935) and operation_start_date>='2022-01-01'	
) as sub


select reg_code, sum(requested_power)
from reply_from_iec_inc_enum as a	
where reg_code not in (280, 290, 905, 935) and reply_date>='2022-01-01'	
group by reg_code;

select reg_code, count(*) as c, sum(requested_power) as req_power
from reply_from_iec_inc_enum