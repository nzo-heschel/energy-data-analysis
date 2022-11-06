import pandas as pd
import re

# old data source, not in use:
# path = r"C:\Users\noami\Documents\NZO\yishuv_list_from_gov_site.csv"
# lms_df = pd.read_csv(path)
# col_names = ['yishuv_code', 'yishuv_name', 'region_code', 'region', 'local_council_code', 'local_council']
# lms_df.columns = col_names
# lms_df['yishuv_name'] = lms_df['yishuv_name'].str.strip()

# one-time using the original LMS file and creating the mapping file:
# lms_df = pd.read_csv(r"C:\Users\noami\Documents\NZO\lms_yishuv_list_original.csv")
# lms_df = lms_df.iloc[:, [0, 1, 3, 4, 6, 14]]
# col_names = ['yishuv_name', 'yishuv_code', 'region_code', 'subregion_code', 'municipal_status', 'yishuv_type']
# lms_df.columns = col_names
# lms_df.to_csv(r"C:\Users\noami\Documents\NZO\lms_yishuv_name_list.csv",  index=False, encoding='utf-8-sig')

LMS_PATH = r"../Resources/lms_yishuv_name_to_code_map.csv"
MANUAL_MAP_PATH = r"../Resources/manual_map_of_yishuv_name.csv"

lms_df = pd.read_csv(LMS_PATH)
# col_names = ['yishuv_name', 'yishuv_code', 'region_code', 'subregion_code', 'municipal_status', 'yishuv_type']
# lms_df.columns = col_names
MAXIMAL_YISHUV_CODE = lms_df['yishuv_code'].max()

manual_map_df = pd.read_csv(MANUAL_MAP_PATH, header=None)
col_names = ['yishuv_name', 'lms_yishuv_name']
manual_map_df.columns = col_names


def clean_heb_str_from_punctuation(heb_str):
    heb_str = heb_str.replace('"', '').replace('\'', '').replace('*', '').replace(')', '').replace('(', '').replace('-', ' ')
    heb_str = re.sub('\s+', ' ', heb_str)
    return heb_str

# This function maps a given yishuv name to it's code based on the lamas file. if the yishuv name is not found, it asks the user to
# generate a code or to map it to an existing name (for example 'reut' to 'maccabim reut').

def map_yishuv_name_to_code(yishuv_name):
    global MAXIMAL_YISHUV_CODE
    manual_map_list = manual_map_df['yishuv_name'].dropna().to_list()
    lms_df_yishuv_list = lms_df['yishuv_name'].dropna().to_list()
    if yishuv_name in lms_df_yishuv_list:
        return lms_df[lms_df['yishuv_name']==yishuv_name]['yishuv_code'].values[0]
    for lms_yishuv_name in lms_df_yishuv_list:
        lms_yishuv_name_cl = clean_heb_str_from_punctuation(lms_yishuv_name)
        yishuv_name_cl = clean_heb_str_from_punctuation(yishuv_name)
        if lms_yishuv_name_cl == yishuv_name_cl:
            return lms_df[lms_df['yishuv_name']==lms_yishuv_name]['yishuv_code'].values[0]
        if yishuv_name_cl == lms_yishuv_name_cl.replace('יי', 'י') or lms_yishuv_name_cl == yishuv_name_cl.replace('יי', 'י'):
            return lms_df[lms_df['yishuv_name'] == lms_yishuv_name]['yishuv_code'].values[0]
        if yishuv_name_cl == lms_yishuv_name_cl.replace('וו', 'ו') or lms_yishuv_name_cl == yishuv_name_cl.replace('וו', 'ו'):
            return lms_df[lms_df['yishuv_name'] == lms_yishuv_name]['yishuv_code'].values[0]
        if len(yishuv_name_cl)>7 and len(lms_yishuv_name_cl)-len(yishuv_name_cl)<3 and yishuv_name_cl in lms_yishuv_name_cl:
           return lms_df[lms_df['yishuv_name'] == lms_yishuv_name]['yishuv_code'].values[0]
    if yishuv_name in manual_map_list:
        map_yishuv_name = manual_map_df[manual_map_df['yishuv_name']==yishuv_name]['lms_yishuv_name'].values[0]
        try:
            return lms_df[lms_df['yishuv_name']==map_yishuv_name]['yishuv_code'].values[0]
        except:
            print("The value in the manual mapping does not appear in the LMS file")
    else:
        response = None
        print("The currect yishuv name is " + yishuv_name)
        while response not in {'1', '2', '3'}:
            response = input("choose 1 to manually map the name to existing name in the LMS file or choose 2 to generate code to the yishuv_name" \
                        + "or choose 3 to skip this name: ")

            if response == '1':
                mapped_name = input("insert the correct name from the LMS list: ")
                while mapped_name not in lms_df_yishuv_list:
                    mapped_name = input("Please insert a valid lms name: ")
                with open(MANUAL_MAP_PATH, 'a', encoding='utf-8') as file:
                    file.write(yishuv_name + ',' + mapped_name + '\n')
                manual_map_df.loc[len(manual_map_df.index)] = [yishuv_name, mapped_name]
                return lms_df[lms_df['yishuv_name'] == mapped_name]['yishuv_code'].values[0]
            if response == '2':
                if MAXIMAL_YISHUV_CODE<100000:
                    generated_code = 1000000
                else:
                    generated_code = MAXIMAL_YISHUV_CODE+1
                with open(LMS_PATH, 'a', encoding='utf-8') as file:
                    file.write(yishuv_name + ',' + str(generated_code) + '\n')
                lms_df.loc[len(lms_df.index)] = [yishuv_name, generated_code, 0, 0, 0, 0]
                MAXIMAL_YISHUV_CODE = generated_code
                return generated_code
            if response == '3':
                return -1
        return -1


# path = r"C:\Users\noami\Documents\NZO\list_of_yishuv_from_data.csv"
# yishuv_df = pd.read_csv(path)
# yishuv_df.columns = ['yishuv_name']
# yishuv_df['yishuv_code'] = yishuv_df['yishuv_name'].apply(map_yishuv_name_to_code)
# yishuv_df.to_excel(r"C:\Users\noami\Documents\NZO\map_yishuv_name_to_code.xlsx")

