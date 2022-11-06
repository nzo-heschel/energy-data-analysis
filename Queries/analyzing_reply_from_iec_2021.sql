USE `nzo_db`;

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
	from reply_from_iec as a
    where reg_number not in ('[אסדרה גז טבעי [290', '[אסדרת יצרן ביו-גז [280', '[905] התקנת טורבינת רוח') and reply_date>='2022-01-01'
) as sub
group by req_power_segments
order by req_power_segments

#אסדרות תעריפיות
where reply_date>='2022-01-01' and reg_number in (
'הספק מעבר להספק הפחת עם תוספת ממיר [352]'
,'הספק מעבר להספק הפחת ללא החלפת ממי [351]'
,'[314] שילוב על חיבור חדש'
,'[906] או PV הגדלה/הוספה חיבור לצורך'
,'[251] צריכה עצמית ללא תעריף'
,'[350] החלפת הספק עד להספק פחת'
,'[250] אסדרה תעריפית ברירת מחדל'
,'[305] אסדרה תעריפית עד 15 עם מונה ייצור'
,'[310] מתקנים עד 15'
,'[311] מתקנים מעל 15 ועד 100'
,'[300] ה תעריפית עד 15 קוא ללא מונה ייצור'
,'[312] חיבור מתקן תעריפי עד 630'
,'[308] אסדרה תעריפית מעל 15 קוא'
)


רק אסדרות תעריפיות: 250, 308, 305, 300, 906, 350, 312, 311, 310, 251, 301
select * from reply_from_iec
where reply_date>='2022-01-01'  and requested_power =2000 and reg_number in (
'הספק מעבר להספק הפחת עם תוספת ממיר [352]'
,'הספק מעבר להספק הפחת ללא החלפת ממי [351]'
,'[314] שילוב על חיבור חדש'
,'[906] או PV הגדלה/הוספה חיבור לצורך'
,'[251] צריכה עצמית ללא תעריף'
,'[350] החלפת הספק עד להספק פחת'
,'[250] אסדרה תעריפית ברירת מחדל'
,'[305] אסדרה תעריפית עד 15 עם מונה ייצור'
,'[310] מתקנים עד 15'
,'[311] מתקנים מעל 15 ועד 100'
,'[300] ה תעריפית עד 15 קוא ללא מונה ייצור'
,'[312] חיבור מתקן תעריפי עד 630'
,'[308] אסדרה תעריפית מעל 15 קוא'
)
רק אסדרות תחרותיות: 133, 134, 160, 140, 141, 142, 170, 171, 940, 260
where reg_number in (']133[ בור פיוי בינוני הליך תחרותי מכרז 3', ']134[ בור פיוי בינוני הליך תחרותי מכרז 4', '[ה.תחרותי גגות ללא מכרז [160', ']140[ חיבור פיוי הליך תחרותי גגות מכרז 1', ']141[ חיבור פיוי הליך תחרותי גגות מכרז 2',
']142[ חיבור פיוי הליך תחרותי גגות מכרז 3', ']170[ בשילוב קיבולת אגירה מכרז 1 PV יבור', ']171[ בשילוב קיבולת אגירה מכרז 2 PV יבור', '[יצרן פרטי [940', ']260[ מחלק היסטורי אסדרות חדשות 2018')

select reg_number, count(*) as c
from reply_from_iec
group by 1

select reg_number, requested_power, count(*) 
from reply_from_iec
where reply_date>='2022-01-01' and requested_power between 101 and 200 and reg_number in (
'הספק מעבר להספק הפחת עם תוספת ממיר [352]'
,'הספק מעבר להספק הפחת ללא החלפת ממי [351]'
,'[314] שילוב על חיבור חדש'
,'[906] או PV הגדלה/הוספה חיבור לצורך'
,'[251] צריכה עצמית ללא תעריף'
,'[350] החלפת הספק עד להספק פחת'
,'[250] אסדרה תעריפית ברירת מחדל'
,'[305] אסדרה תעריפית עד 15 עם מונה ייצור'
,'[310] מתקנים עד 15'
,'[311] מתקנים מעל 15 ועד 100'
,'[300] ה תעריפית עד 15 קוא ללא מונה ייצור'
,'[312] חיבור מתקן תעריפי עד 630'
,'[308] אסדרה תעריפית מעל 15 קוא'
)
group by 1, 2

select 
napa,
iec_reply,
sum(requested_power)/1000 as sum_req_power
from reply_from_iec
group by 1, 2

select 
req_power_segments
,sum(requested_power) as total_requested_power_kw
,count(id) as num_of_requests
from (
	select 
	a.*
	,case when requested_power<15 then '0-14' 
		when requested_power=15 then '015'
		when requested_power between 16 and 199 then '016-199'
		when requested_power =200 then '200'
		when requested_power between 201 and 630 then '201-630'
        when requested_power >630 then 'higher_than_630'
		end as req_power_segments
	from reply_from_iec as a
    where reg_number not in ('[אסדרה גז טבעי [290', '[אסדרת יצרן ביו-גז [280')
    ##where reg_number in ('[אסדרה תעריפית ברירת מחדל [250', '[אסדרה תעריפית מעל 15 קוא [308', '[אסדרה תעריפית עד 15 עם מונה ייצור [305', '[ה תעריפית עד 15 קוא ללא מונה ייצור [300', '[או [906 PV הגדלה/הוספה חיבור לצורך', 
	##'[החלפת הספק עד להספק פחת [350', ']312[ חיבור מתקן תעריפי עד 630', ']311[ מתקנים מעל 15 ועד 100', ']310[ מתקנים עד 15', '[צריכה עצמית ללא תעריף [251', '[ללא מונה ייצור ו [301 KVA 15 תעריפית עד')
    ##where reg_number in (']133[ בור פיוי בינוני הליך תחרותי מכרז 3', ']134[ בור פיוי בינוני הליך תחרותי מכרז 4', '[ה.תחרותי גגות ללא מכרז [160', ']140[ חיבור פיוי הליך תחרותי גגות מכרז 1', ']141[ חיבור פיוי הליך תחרותי גגות מכרז 2',
	##']142[ חיבור פיוי הליך תחרותי גגות מכרז 3', ']170[ בשילוב קיבולת אגירה מכרז 1 PV יבור', ']171[ בשילוב קיבולת אגירה מכרז 2 PV יבור', '[יצרן פרטי [940', ']260[ מחלק היסטורי אסדרות חדשות 2018')
) as sub
group by req_power_segments
order by req_power_segments

select 
requested_power
,count(id) as num_of_requests
from reply_from_iec as a
where reg_number not in ('[אסדרה גז טבעי [290', '[אסדרת יצרן ביו-גז [280') and reply_date>='2022-01-01'
group by requested_power
order by requested_power


select 
case 	when reply_date>='2022-01-01' then '22-q1' 
		when reply_date between '2021-01-01' and '2021-03-31' then '21-q1'
        when reply_date between '2021-04-01' and '2021-06-30' then '21-q2'
        when reply_date between '2021-07-01' and '2021-09-30' then '21-q3'
		when reply_date between '2021-10-01' and '2021-12-31' then '21-q4' 
end as Q
,a.yishuv_code as municipal_status
,iec_reply_code
,count(id) as num_of_requests
,sum(requested_power) as sum_of_requested_power
/*,avg(requested_power) as ave_of_requested_power*/
from reply_from_iec_inc_enum as a
left join lms_yishuv_name_to_code_map as b on a.yishuv_code = b.yishuv_code
where reg_code not in (280, 290) /*gas regulations*/  and a.yishuv_code in (1000043, 1000029)
group by Q, a.yishuv_code, iec_reply_code
order by a.yishuv_code, Q, iec_reply_code






select 
min(requested_power, 15)*48+max(min(requested_power, 15), 0)


select min(requested_power, 15)