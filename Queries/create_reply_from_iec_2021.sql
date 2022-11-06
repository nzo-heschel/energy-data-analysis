USE `nzo_db`;

SET NAMES utf8mb4 ;
SET character_set_client = utf8mb4 ;
SET GLOBAL local_infile = true;

DROP TABLE reply_from_iec_inc;
CREATE TABLE reply_from_iec_inc (
            id INT NOT NULL AUTO_INCREMENT,
            agaf VARCHAR(60) NOT NULL,
            napa VARCHAR(60) NOT NULL,
            yishuv VARCHAR(60) NOT NULL,
            reg_number VARCHAR(60) NOT NULL,
            requested_power INT NOT NULL,
            voltage VARCHAR(60) NOT NULL,
            iec_reply VARCHAR(60) NOT NULL,
            reply_date VARCHAR(12) NOT NULL,
            PRIMARY KEY (id)
);

--add checks on the increment table
--after passing checks, add the data to the main table
select count(*) from reply_from_iec_inc --16734, 19534
select * from reply_from_iec_inc where id>16730

select yishuv, count(*) as c 
from reply_from_iec_inc
group by 1


--changing bad yishuv names:
select * from reply_from_iec_inc
where yishuv = 'מודיעין מכבים רעו'

UPDATE reply_from_iec_inc
SET 
    yishuv = 'מודיעין מכבים רעות'
WHERE id in (2373, 6673, 8274, 16328)
    

DROP TABLE reply_from_iec_inc_enum;
CREATE TABLE reply_from_iec_inc_enum (
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

select count(*) from reply_from_iec_inc_enum
select * from reply_from_iec_inc_enum where reply_date>'2022-01-01'



DROP TABLE connection_to_the_grid;
CREATE TABLE connection_to_the_grid (
            id INT NOT NULL,
            agaf VARCHAR(60) NOT NULL,
            napa VARCHAR(60) NOT NULL,
            yishuv VARCHAR(60) NOT NULL,
            reg_number VARCHAR(60) NOT NULL,
            requested_power INT NOT NULL,
            voltage VARCHAR(60) NOT NULL,
            operation_start_date date NOT NULL,
            PRIMARY KEY (id)
);

DROP TABLE connection_to_the_grid_enum;
CREATE TABLE connection_to_the_grid_enum (
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


select max(operation_start_date) from connection_to_the_grid_enum; 
select * from connection_to_the_grid_enum where operation_start_date > '2022-03-30';


SHOW VARIABLES LIKE "secure_file_priv";
SHOW GLOBAL VARIABLES LIKE "local_infile"; 


select
month(operation_start_date) as mth,
count(*) as cnt_connections
from connection_to_the_grid
where reg_number not in ('[אסדרה גז טבעי [290', '[אסדרת יצרן ביו-גז [280') ## without gas
group by 1
order by 1


--DEPRECARTED:
LOAD DATA LOCAL INFILE 'C:/Users/noami/Documents/NZO/chibur_lareshet_2021_csv.csv'
INTO TABLE connection_to_the_grid
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;

