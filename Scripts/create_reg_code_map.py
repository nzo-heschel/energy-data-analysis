import os.path
from pdf_as_txt_to_sql_or_excel import parse_txt_file, extract_number_from_field

REG_CODE_MAP_PATH = r"../Resources/reg_number_map.txt"

# The function updates or creates the registration code map with a new chibur lareshet ('c') or tshuvat mechalek ('t') files.

def create_or_update_reg_code_map(file_path, file_type, reg_code_field_name='reg_number', write_back_to_file_yn='n'):
    reg_number_map = {}
    if os.path.exists(REG_CODE_MAP_PATH):
        with open(REG_CODE_MAP_PATH, encoding='UTF-8') as txt:
            for line in txt:
                (key, val) = line.replace('\'', '').replace('\n', '').strip().split(',')
                reg_number_map[int(key)] = val
    df = parse_txt_file(file_path, file_type)
    reg_field_list = df[reg_code_field_name].drop_duplicates().tolist()
    for val in reg_field_list:
        reg_code = extract_number_from_field(val)
        if len(reg_code)>0 and int(reg_code) not in reg_number_map.keys():
            desc_val = val.replace(reg_code, '').replace(']', '').replace('[', '').strip()
            reg_number_map[int(reg_code)] = desc_val
    if write_back_to_file_yn == 'y':
        with open(REG_CODE_MAP_PATH, 'w', encoding='UTF-8') as f:
            for k in sorted(reg_number_map.keys()):
                f.write("'%s', '%s'\n" % (k, reg_number_map[k]))
    return reg_number_map


VOLTAGE_MAP_PATH = r"../Resources/voltage_map.txt"

# The function updates or creates the registration code map with a new chibur lareshet ('c') or tshuvat mechalek ('t') files.

def create_or_update_codes_map(file_path, file_type, code_map_path, field_name, write_back_to_file_yn='n'):
    code_map = {}
    if os.path.exists(code_map_path):
        with open(code_map_path, encoding='UTF-8') as txt:
            for line in txt:
                (key, val) = line.replace('\'', '').replace('\n', '').strip().split(',')
                code_map[int(key)] = val
    df = parse_txt_file(file_path, file_type)
    field_list = df[field_name].drop_duplicates().tolist()
    for val in field_list:
        code = extract_number_from_field(val)
        if len(code)>0 and int(code) not in code_map.keys():
            desc_val = val.replace(code, '').replace(']', '').replace('[', '').strip()
            code_map[int(code)] = desc_val
    if write_back_to_file_yn == 'y':
        with open(code_map_path, 'w', encoding='UTF-8') as f:
            for k in sorted(code_map.keys()):
                f.write("'%s', '%s'\n" % (k, code_map[k]))
    return code_map


