import pandas as pd
import re
from upload_data_to_mysql import upload_df_to_mysql
from map_yishuv_name_to_code import *
import txt_field_mapping as fld_val

#r"C:\Users\noami\Documents\NZO\chibur_lareshet_2021.txt"
#r"C:\Users\noami\Documents\NZO\tshuvat_mechalek_q1_2022.txt"

# def ask_user():
#     res = input("Choose t for tshuvat mechalek or c for chibur laresht").lower()
#     while res not in {'t', 'c'}:
#         res = input("Choose t for tshuvat mechalek or c for chibur laresht").lower()
#     return res

#REG_CODE_MAP_PATH = r"C:\Users\noami\Documents\NZO\mappings\reg_number_map.txt"

def extract_number_from_field(fld):
    #res = re.findall(r'(.*)(\[|\])(\d+)(\[|\])(.*)', fld)
    res = re.findall(r'] (.*)\] (\d+)', fld)
    if len(res)>0:
        return res[0][1]
    #res = re.findall(r'](\d+)\[(.*)', fld)
    res = re.findall(r'(.*)(\[|\])(\d+)(\[|\])(.*)', fld)
    if len(res)>0:
        return res[0][2]
    res = re.findall(r'(.+) (\d+) ](.+)]', fld)
    if len(res)>0:
        return res[0][1]
    return ''

def set_date_format(date_str):
    return re.sub(r'((\d){2})\/((\d){2})\/((\d){4})', r'\5-\3-\1', date_str)

def map_field_values_to_enum(field_name, value):
    if field_name not in ['voltage', 'iec_reply']:
        return print('Wrong field_name. Should be voltage or iec_reply')
    if field_name == 'voltage':
        if value not in fld_val.VOLTAGE_VALUE_MAPPING.keys():
            return print(str(value)+' value not found in mapping')
        return fld_val.VOLTAGE_VALUE_MAPPING[value]
    if field_name == 'iec_reply':
        if value not in fld_val.IEC_REPLY_VALUE_MAPPING.keys():
            return print(str(value)+' value not found in mapping')
        return fld_val.IEC_REPLY_VALUE_MAPPING[value]


def parse_txt_file(file_path, file_type):
    if file_type == 'c':
        NUM_COLUMNS = 8
        TABLE_COL_NAMES = ['id', 'agaf', 'napa', 'yishuv', 'reg_number', 'requested_power', 'voltage',
                           'operation_start_date']
    if file_type == 't':
        NUM_COLUMNS = 9
        TABLE_COL_NAMES = ['id', 'agaf', 'napa', 'yishuv', 'reg_number', 'requested_power', 'voltage', 'iec_reply',
                           'reply_date']
    with open(file_path, encoding="UTF-8") as txt:
        lines = []
        for t in txt:
            lines.append(t)
    nl = []
    j=0
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '').strip()
        if lines[i] == '':
            continue
        else:
            if i==0:
                nl.append(lines[i])
            elif lines[i-1]=='':
                j=j+1
                nl.append(lines[i])
            else:
                nl[j] = nl[j]+' '+lines[i]
    rows = []
    new_list = []
    for i in range(len(nl)):
        col = i%NUM_COLUMNS
        new_list.append(nl[i])
        if col == NUM_COLUMNS-1:
            rows.append(new_list)
            new_list = []
    new_df = pd.DataFrame(rows[1:], columns=TABLE_COL_NAMES)
    return new_df

def process_txt_file(file_path, file_type, excel_output_path='', sql_table_name=''):
    if file_type not in ['t', 'c']:
        return print("Invalid file type. please insert t for tshuvat mechalek or c for chibur laresht")
    if file_type == 'c':
#        NUM_COLUMNS = 8
#        TABLE_COL_NAMES = ['id', 'agaf', 'napa', 'yishuv', 'reg_number', 'requested_power', 'voltage',
#                           'operation_start_date']
#        EXCEL_OUTPUT_PATH = r'C:\Users\noami\Documents\NZO\chibur_lareshet_increment.xlsx'
#        SQL_TABLE_NAME = 'connection_to_the_grid_inc'
        DATE_COLUMN = 'operation_start_date'
    if file_type == 't':
#        NUM_COLUMNS = 9
#        TABLE_COL_NAMES = ['id', 'agaf', 'napa', 'yishuv', 'reg_number', 'requested_power', 'voltage', 'iec_reply', 'reply_date']
#        EXCEL_OUTPUT_PATH = r'C:\Users\noami\Documents\NZO\tshuvat_mechalek_increment.xlsx'
#        SQL_TABLE_NAME = 'reply_from_iec_inc'
        DATE_COLUMN = 'reply_date'
    new_df = parse_txt_file(file_path, file_type)
    new_df['agaf_code'] = new_df['agaf'].apply(extract_number_from_field)
    new_df['napa_code'] = new_df['napa'].apply(extract_number_from_field)
    new_df['yishuv_code'] = new_df['yishuv'].apply(map_yishuv_name_to_code)
    new_df['reg_code'] = new_df['reg_number'].apply(extract_number_from_field)
    #need to update the reg code mapping with new records
    if ('[' in new_df['voltage'][1] or ']' in new_df['voltage'][1]):
        new_df['voltage_code'] = new_df['voltage'].apply(extract_number_from_field)
    else:
        new_df['voltage_code'] = new_df['voltage'].apply(lambda x: map_field_values_to_enum('voltage', x))
        if 'value not found in mapping' in new_df['voltage_code'].values:
            print('There are new values in voltage column')
    new_df[DATE_COLUMN] = new_df[DATE_COLUMN].apply(set_date_format)
    if file_type == 't':
        if ('[' in new_df['iec_reply'][1] or ']' in new_df['iec_reply'][1]):
            new_df['iec_reply_code'] = new_df['iec_reply'].apply(extract_number_from_field)
        else:
            new_df['iec_reply_code'] = new_df['iec_reply'].apply(lambda x: map_field_values_to_enum('iec_reply', x))
            if 'value not found in mapping' in new_df['voltage_code'].values:
                print('There are new values in iec_reply column')
        new_df = new_df[['id', 'agaf_code', 'napa_code', 'yishuv_code', 'reg_code', 'requested_power', 'voltage_code',
                         'iec_reply_code', 'reply_date']]
    if file_type == 'c':
        new_df = new_df[['id', 'agaf_code', 'napa_code', 'yishuv_code', 'reg_code', 'requested_power', 'voltage_code',
                         'operation_start_date']]

    if excel_output_path!='':
        new_df.to_excel(excel_output_path)
    if sql_table_name!='':
        upload_df_to_mysql(new_df.loc[:, new_df.columns != 'id'], sql_table_name)
    return new_df



# ##lines[i] = lines[i].replace('\n', '').strip().replace('] ', '**').replace('] ', ']').replace('**', '[')
# lines[i] = lines[i].replace('\n', '').strip()
# lines[i] = lines[i].replace('  ', ' ').strip()
# #lines[i] = re.sub(r'] (.*)\] (\d+)', r'\1 [\2]', lines[i])
# lines[i] = re.sub(r'] (.*)\] (\d+)', r'[\2] \1', lines[i])
# # lines[i] = re.sub(r'](\d+)\[(.*)', r'\2[\1]', lines[i]).strip()
# lines[i] = re.sub(r'](\d+)\[(.*)', r'[\1] \2', lines[i]).strip()
# lines[i] = re.sub(r'((\d){2})\/((\d){2})\/((\d){4})', r'\5-\3-\1', lines[i])  #change the date to mysql date format
# lines[i] = lines[i].replace('  ', ' ').strip()

