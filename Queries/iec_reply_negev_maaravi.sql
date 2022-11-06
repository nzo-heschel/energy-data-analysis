USE `nzo_db`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;

select 	
Q
,case 	when municipality=36 then 'Hof_Ashkelon'
		when municipality=37 then 'Shaar_Hanegev'
        when municipality=38 then 'Eshkol'
		when municipality=39 then 'Sdot_Negev'
		when municipality=100000 then 'Sderot'
end as municipality_name
,case 	when iec_reply_code=1 then 'positive'
		when iec_reply_code=2 then 'positive_partial'
        when iec_reply_code=3 then 'positive_limited'
        when iec_reply_code=4 then 'negative'
end as iec_reply
,case 	when voltage_code=1 then 'low_voltage'
		when voltage_code=2 then 'high_voltage'
end as voltage
,num_of_requests
,sum_of_requested_power
from (
	select 
	case 	when reply_date>='2022-01-01' then '22-q1' 
			when reply_date between '2021-01-01' and '2021-03-31' then '21-q1'
			when reply_date between '2021-04-01' and '2021-06-30' then '21-q2'
			when reply_date between '2021-07-01' and '2021-09-30' then '21-q3'
			when reply_date between '2021-10-01' and '2021-12-31' then '21-q4' 
	end as Q
	,case 	when a.yishuv_code=1000029 then 39
			when a.yishuv_code=1000043 then 36
			when a.yishuv_code=1031 then 100000 /*Sderot*/
			else b.municipal_status
	end as municipality
	,voltage_code
	,iec_reply_code
	,count(id) as num_of_requests
	,sum(requested_power) as sum_of_requested_power
	from reply_from_iec_inc_enum as a
	left join lms_yishuv_name_to_code_map as b on a.yishuv_code = b.yishuv_code
	where reg_code not in (280, 290) /*gas regulations*/ 
	group by Q, municipality, voltage_code, iec_reply_code
) as sub
where municipality in (36, 37, 38, 39, 100000)
order by municipality, Q, voltage_code, iec_reply_code



select max(municipal_status) from lms_yishuv_name_to_code_map