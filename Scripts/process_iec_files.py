import os.path
import sys
import pandas as pd
import re
import pymysql
import sqlalchemy
import argparse

REG_CODE_MAP_PATH = r"../Resources/reg_number_map.txt"
VOLTAGE_CODE_MAP_PATH = r"../Resources/voltage_map.txt"
AGAF_CODE_MAP_PATH = r"../Resources/agaf_map.txt"
NAPA_CODE_MAP_PATH = r"../Resources/napa_map.txt"
IEC_REPLY_CODE_MAP_PATH = r"../Resources/iec_reply_map.txt"
LMS_PATH = r"../Resources/lms_yishuv_name_to_code_map.csv"
MANUAL_MAP_PATH = r"../Resources/manual_map_of_yishuv_name.csv"

def clean_punctuation_from_heb_str(heb_str):
    heb_str = heb_str.replace('"', '').replace('\'', '').replace('*', '').replace(')', '').replace('(', '').replace('-', ' ')
    heb_str = re.sub('\s+', ' ', heb_str)
    return heb_str

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
        return fld_val.VOLTAGE_VALUE_MAPPING[value]
    if field_name == 'iec_reply':
        return fld_val.IEC_REPLY_VALUE_MAPPING[value]

# The function updates or creates the code map with a new chibur lareshet ('c') or tshuvat mechalek ('t') files.

def create_or_update_code_map_from_df(df, code_map_path, field_name, write_back_to_file=False):
    code_map = {}
    if os.path.exists(code_map_path):
        with open(code_map_path, encoding='UTF-8') as txt:
            for line in txt:
                (key, val) = line.replace('\'', '').replace('\n', '').strip().split(',')
                code_map[int(key)] = val
    values_list = df[field_name].drop_duplicates().tolist()
    for val in values_list:
        code = extract_number_from_field(val)
        if len(code)>0 and int(code) not in code_map.keys():
            desc_val = val.replace(code, '').replace(']', '').replace('[', '').strip()
            code_map[int(code)] = desc_val
    if write_back_to_file == True:
        with open(code_map_path, 'w', encoding='UTF-8') as f:
            for k in sorted(code_map.keys()):
                f.write("'%s', '%s'\n" % (k, code_map[k]))
    print(field_name+ ' Code Map Update Completed')
    return code_map

def create_or_update_code_map_from_file(file_path, file_type, code_map_path, field_name, write_back_to_file=False):
    df = parse_txt_file(file_path, file_type)
    return create_or_update_code_maps_from_df(df, code_map_path, field_name, write_back_to_file)


# LMS_PATH column names: col_names = ['yishuv_name', 'yishuv_code', 'region_code', 'subregion_code', 'municipal_status', 'yishuv_type']
# lms_df.columns = col_names

# The function updates yishuv code files using new chibur lareshet ('c') or tshuvat mechalek ('t') files.

def create_or_update_yishuv_code_map_from_df(df, code_map_path=LMS_PATH, manual_map_path=MANUAL_MAP_PATH, field_name='yishuv'):
    lms_df = pd.read_csv(code_map_path)
    MAXIMAL_YISHUV_CODE = lms_df['yishuv_code'].max()
    lms_df_yishuv_list = lms_df['yishuv_name'].dropna().to_list()
    lms_yishuv_name_cl_list = [clean_punctuation_from_heb_str(val) for val in lms_df_yishuv_list]

    manual_map_df = pd.read_csv(manual_map_path, header=None)
    col_names = ['yishuv_name', 'lms_yishuv_name']
    manual_map_df.columns = col_names
    manual_map_list = manual_map_df['yishuv_name'].dropna().to_list()

    field_list = df[field_name].drop_duplicates().tolist()
    for val in field_list:
        if val in lms_df_yishuv_list:
            continue
        if val in manual_map_list:
            continue
        yishuv_name_cl = clean_punctuation_from_heb_str(val)
        if yishuv_name_cl in lms_yishuv_name_cl_list:
            continue
        if yishuv_name_cl.replace('יי', 'י').replace('וו', 'ו') in [val.replace('יי', 'י').replace('וו', 'ו') for val in lms_yishuv_name_cl_list]:
            continue
        response = None
        print("The currect yishuv name is " + val)
        while response not in {'1', '2', '3'}:
            response = input(
                "choose 1 to manually map the name to existing name in the LMS file or choose 2 to generate code to the yishuv_name" \
                + "or choose 3 to skip this name: ")
            if response == '1':
                mapped_name = input("insert the correct name from the LMS list: ")
                while mapped_name not in lms_df_yishuv_list:
                    mapped_name = input("Please insert a valid lms name: ")
                with open(manual_map_path, 'a', encoding='utf-8') as file:
                    file.write(val + ',' + mapped_name + '\n')
                manual_map_df.loc[len(manual_map_df.index)] = [val, mapped_name]
                continue
            if response == '2':
                if MAXIMAL_YISHUV_CODE < 100000:
                    generated_code = 1000000
                else:
                    generated_code = MAXIMAL_YISHUV_CODE + 1
                with open(code_map_path, 'a', encoding='utf-8') as file:
                    file.write(val + ',' + str(generated_code) + '\n')
                lms_df.loc[len(lms_df.index)] = [val, generated_code, 0, 0, 0, 0]
                MAXIMAL_YISHUV_CODE = generated_code
                continue
            if response == '3':
                continue

    print("Yishuv Code Update Completed")
    return lms_df


def create_or_update_yishuv_code_map_from_file(file_path, file_type, code_map_path=LMS_PATH, manual_map_path=MANUAL_MAP_PATH, field_name='yishuv'):
    df = parse_txt_file(file_path, file_type)
    return create_or_update_yishuv_code_map_from_file(df, code_map_path, manual_map_path, field_name)

# one-time using the original LMS file and creating the mapping file:
# lms_df = pd.read_csv(r"C:\Users\noami\Documents\NZO\lms_yishuv_list_original.csv")
# lms_df = lms_df.iloc[:, [0, 1, 3, 4, 6, 14]]
# col_names = ['yishuv_name', 'yishuv_code', 'region_code', 'subregion_code', 'municipal_status', 'yishuv_type']
# lms_df.columns = col_names
# lms_df.to_csv(r"C:\Users\noami\Documents\NZO\lms_yishuv_name_list.csv",  index=False, encoding='utf-8-sig')

# This function maps a given yishuv name to its code based on the lamas file. if the yishuv name is not found, it asks the user to
# generate a code or to map it to an existing name (for example 'reut' to 'maccabim reut').

def map_yishuv_name_to_code(yishuv_name, code_map=LMS_PATH, manual_map=MANUAL_MAP_PATH):
    lms_df = pd.read_csv(code_map)
    manual_map_df = pd.read_csv(manual_map, header=None)
    col_names = ['yishuv_name', 'lms_yishuv_name']
    manual_map_df.columns = col_names
    manual_map_list = manual_map_df['yishuv_name'].dropna().to_list()
    lms_df_yishuv_list = lms_df['yishuv_name'].dropna().to_list()
    lms_yishuv_name_cl_list = [clean_punctuation_from_heb_str(val) for val in lms_df_yishuv_list]
    if yishuv_name in lms_df_yishuv_list:
        return lms_df[lms_df['yishuv_name']==yishuv_name]['yishuv_code'].values[0]
    if yishuv_name in manual_map_list:
        map_yishuv_name = manual_map_df[manual_map_df['yishuv_name']==yishuv_name]['lms_yishuv_name'].values[0]
        try:
            return lms_df[lms_df['yishuv_name']==map_yishuv_name]['yishuv_code'].values[0]
        except:
            print("The value in the manual mapping does not appear in the LMS file")
    yishuv_name_cl = clean_punctuation_from_heb_str(yishuv_name)
    try:
        i = lms_yishuv_name_cl_list.index(yishuv_name_cl)
        return lms_df[lms_df['yishuv_name'] == lms_df.iloc[i, 0]]['yishuv_code'].values[0]
    except Exception:
        pass
    try:
        i = [val.replace('יי', 'י').replace('וו', 'ו') for val in lms_yishuv_name_cl_list].index(yishuv_name_cl.replace('יי', 'י').replace('וו', 'ו'))
        return lms_df[lms_df['yishuv_name'] == lms_df.iloc[i, 0]]['yishuv_code'].values[0]
    except Exception:
        pass
    return -1

def parse_txt_file(file_path: str, file_type: str):
    if file_type == 'c':
        NUM_COLUMNS = 8
        TABLE_COL_NAMES = ['id', 'agaf', 'napa', 'yishuv', 'reg_number', 'requested_power', 'voltage',
                           'operation_start_date']
        DATE_COLUMN = 'operation_start_date'
    if file_type == 't':
        NUM_COLUMNS = 9
        TABLE_COL_NAMES = ['id', 'agaf', 'napa', 'yishuv', 'reg_number', 'requested_power', 'voltage', 'iec_reply',
                           'reply_date']
        DATE_COLUMN = 'reply_date'
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
    new_df[DATE_COLUMN] = new_df[DATE_COLUMN].apply(set_date_format)
    return new_df


def map_value_to_code_with_backwards_compatibility(df, field_name):
    field_name_code = field_name+'_code'
    if ('[' in df[field_name][1] or ']' in df[field_name][1]):
        df[field_name_code] = df[field_name].apply(extract_number_from_field)
    else:
        df[field_name_code] = df[field_name].apply(lambda x: map_field_values_to_enum(field_name, x))
    return df[field_name_code]

def process_txt_file(file_path, file_type, excel_output_path='', sql_table_name=''):
    #ADD: download pdf from website
    #ADD: save pdf as text
    if file_type not in ['t', 'c']:
        return print("Invalid file type. please insert t for tshuvat mechalek or c for chibur laresht")
    new_df = parse_txt_file(file_path, file_type)

    #updating static tables with new values from new files
    temp = create_or_update_code_map_from_df(new_df, AGAF_CODE_MAP_PATH, 'agaf', write_back_to_file=True)
    temp = create_or_update_code_map_from_df(new_df, NAPA_CODE_MAP_PATH, 'napa', write_back_to_file=True)
    temp = create_or_update_code_map_from_df(new_df, REG_CODE_MAP_PATH, 'reg_number', write_back_to_file=True)
    temp = create_or_update_code_map_from_df(new_df, VOLTAGE_CODE_MAP_PATH, 'voltage', write_back_to_file=True)
    temp = create_or_update_yishuv_code_map_from_df(new_df)
    if file_type == 't':
        temp = create_or_update_code_map_from_df(new_df, IEC_REPLY_CODE_MAP_PATH, 'iec_reply', write_back_to_file=True)

    new_df['agaf_code'] = new_df['agaf'].apply(extract_number_from_field)
    new_df['napa_code'] = new_df['napa'].apply(extract_number_from_field)
    new_df['yishuv_code'] = new_df['yishuv'].apply(map_yishuv_name_to_code)
    new_df['reg_code'] = new_df['reg_number'].apply(extract_number_from_field)

    #Supports older IEC files where there were no codes for voltage and iec_reply
    new_df['voltage_code'] = map_value_to_code_with_backwards_compatibility(new_df, 'voltage')
    if file_type == 't':
        new_df['iec_reply_code'] = map_value_to_code_with_backwards_compatibility(new_df, 'iec_reply')
        new_df = new_df[['id', 'agaf_code', 'napa_code', 'yishuv_code', 'reg_code', 'requested_power', 'voltage_code',
                         'iec_reply_code', 'reply_date']]
    if file_type == 'c':
        new_df = new_df[['id', 'agaf_code', 'napa_code', 'yishuv_code', 'reg_code', 'requested_power', 'voltage_code',
                         'operation_start_date']]

    # if excel_output_path!='':
    #     new_df.to_excel(excel_output_path)
    # if sql_table_name!='':
    #     upload_df_to_mysql(new_df.loc[:, new_df.columns != 'id'], sql_table_name)
    return new_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process IEC file and extract output in the required form (dataframe, excel or SQL)')
    parser.add_argument("file_path", help="the path of the iec file as text to process")
    parser.add_argument("file_type", choices=['t', 'c'], help="t for tshuvat mechalek or c for chibur laresht")
    subparser = parser.add_subparsers(dest='output', help='Choose how you want to handle the output')
    as_df = subparser.add_parser('as_df', help='Keep the output as dataframe')
    excel = subparser.add_parser('excel', help='Extract the output to excel file')
    sql = subparser.add_parser('sql', help='Upload the data to MySQL')
    excel.add_argument("output_path", help="The path of the excel file to be saved")
    sql.add_argument("user", help="your MySQL username")
    sql.add_argument("pwd", help="your MySQL password")
    #parser.add_argument("port", type=int, default=3306, help="your MySQL port")
    sql.add_argument("--database", default='nzo_db', help="The database to which you want to connect")
    sql.add_argument("--host", default='localhost', help="your MySQL host")
    #sql.add_argument("df", help="The data to upload as a DataFrame", required=True)
    sql.add_argument("tablename", help="The table name to which you want to append the data")
    sql.add_argument("--if_exists", default='append', help="What to do if table already exists. options: {‘fail’, ‘replace’, ‘append’}")
    sql.add_argument("--index", action='store_true', help="Write DataFrame index True or False. The default is False")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


    if args.output == 'as_df':
        df = process_txt_file(args.file_path, args.file_type)
    if args.output == 'excel':
        df = process_txt_file(args.file_path, args.file_type)
        df.to_excel(args.output_path)
    if args.output == 'sql':
        df = process_txt_file(args.file_path, args.file_type)
        if args.index == False:
            df = df.loc[:, df.columns != 'id']
        database_connection = sqlalchemy.create_engine(
                'mysql+pymysql://{0}:{1}@{2}/{3}'.format(args.user, args.pwd, args.host, args.database))
        df.to_sql(con=database_connection, name=args.tablename, if_exists=args.if_exists, index=args.index)






# ##lines[i] = lines[i].replace('\n', '').strip().replace('] ', '**').replace('] ', ']').replace('**', '[')
# lines[i] = lines[i].replace('\n', '').strip()
# lines[i] = lines[i].replace('  ', ' ').strip()
# #lines[i] = re.sub(r'] (.*)\] (\d+)', r'\1 [\2]', lines[i])
# lines[i] = re.sub(r'] (.*)\] (\d+)', r'[\2] \1', lines[i])
# # lines[i] = re.sub(r'](\d+)\[(.*)', r'\2[\1]', lines[i]).strip()
# lines[i] = re.sub(r'](\d+)\[(.*)', r'[\1] \2', lines[i]).strip()
# lines[i] = re.sub(r'((\d){2})\/((\d){2})\/((\d){4})', r'\5-\3-\1', lines[i])  #change the date to mysql date format
# lines[i] = lines[i].replace('  ', ' ').strip()

