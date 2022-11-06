CREATE DATABASE IF NOT EXISTS `nzo_db`;
USE `nzo_db`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;
SET GLOBAL local_infile = true;

drop table lms_yishuv_name_to_code_map
CREATE TABLE `lms_yishuv_name_to_code_map` (
  `yishuv_name` VARCHAR(60) NOT NULL,
  `yishuv_code` int NOT NULL,
  `region_code` int,
  `subregion_code` int,
  `municipal_status` int,
  `yishuv_type` int,
  PRIMARY KEY (`yishuv_code`)
) ENGINE=InnoDB;

LOAD DATA LOCAL INFILE 'C:/Users/noami/Documents/NZO/mappings/lms_yishuv_name_to_code_map.csv'
INTO TABLE lms_yishuv_name_to_code_map
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;

select * from lms_yishuv_name_to_code_map order by yishuv_name;

CREATE TABLE reg_code_to_value_mapping (
            reg_code INT,
            reg_value VARCHAR(200) NOT NULL,
            PRIMARY KEY (reg_code)
);

LOAD DATA LOCAL INFILE 'C:/Users/noami/Documents/NZO/mappings/reg_number_map.txt'
INTO TABLE reg_code_to_value_mapping
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;

select * from reg_code_to_value_mapping
