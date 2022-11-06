USE `nzo_db`;
1397 - conncetions with no matchs in reply_from_iec_2021, 19.2%
7253 - total number of records in connection_to_the_grid

select *
from connection_to_the_grid as sub1
left join (select b.id from reply_from_iec_2021 as a
	join connection_to_the_grid as b on a.yishuv=b.yishuv and a.reg_number=b.reg_number
	where a.iec_reply like '%חיובית%' and a.reply_date<b.operation_start_date and a.requested_power>=b.requested_power
	group by b.id
) as sub2 on sub1.id=sub2.id
where sub2.id is null 

select a.*, b.requested_power, b.operation_start_date
from reply_from_iec_2021 as a
join connection_to_the_grid as b on a.yishuv=b.yishuv and a.reg_number=b.reg_number
where a.iec_reply like '%חיובית%' and a.reply_date<b.operation_start_date and a.requested_power>=b.requested_power
limit 100

select a.*, b.requested_power, b.operation_start_date
from reply_from_iec_2021 as a
join connection_to_the_grid as b on a.yishuv=b.yishuv and a.reg_number=b.reg_number
where a.iec_reply like '%חיובית%' and a.reply_date<b.operation_start_date and a.requested_power>=b.requested_power and a.yishuv = 'כפר הס'
limit 100
 



