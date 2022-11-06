import pandas as pd
import difflib as dl
import re

# This code is comparing yishuv names between the formal yishuv names file and the yishuv names in the
# chibur lareshet or tshuvat mechalek files. This is a one-time comparison used to create the mapping files for
# map_yishuv_name_to_code.py

#path = r"C:\Users\noami\Documents\NZO\cities_list.csv"
#raw_df = pd.read_csv(path, encoding='utf-8')
#col_names = ['yishuv_code', 'yishuv_name', 'region', 'local_council', 'cluster', 'postal_code']
#raw_df.columns = col_names

path = r"../Resources/yishuv_list_from_gov_site.csv"
raw_df = pd.read_csv(path)
col_names = ['yishuv_code', 'yishuv_name', 'region_code', 'region', 'local_council_code', 'local_council']
raw_df.columns = col_names

path = r"../Resources/list_of_yishuv_from_data.csv"
yishuv_df = pd.read_csv(path)
yishuv_df.columns = ['yishuv_name']

raw_df['yishuv_name'] = raw_df['yishuv_name'].str.strip()
raw_df['yishuv_name'] = raw_df['yishuv_name'].str.replace('"', '')
raw_df['yishuv_name'] = raw_df['yishuv_name'].str.replace('\'', '')
raw_df['yishuv_name'] = raw_df['yishuv_name'].str.replace('\*', '') #need to check if requires the \
raw_df['yishuv_name'] = raw_df['yishuv_name'].str.replace(')', '')
raw_df['yishuv_name'] = raw_df['yishuv_name'].str.replace('(', '')
match_results = pd.merge(yishuv_df, raw_df, how='inner', on='yishuv_name')

#results = pd.merge(yishuv_df, raw_df, how='left', on='yishuv_name')

#results[results["yishuv_code"].isna()].head()
to_match = pd.merge(yishuv_df, match_results, how='left', on='yishuv_name')
to_match = to_match[to_match["yishuv_code"].isna()]['yishuv_name'] #returns a series
to_match = to_match.to_frame()

def close_strings(x):
    if type(x) is not str:
        return '*****' + type(x)
    else:
        list_of_names = raw_df['yishuv_name'].dropna().to_list()
        for n in list_of_names:
            if re.sub('\s+', ' ', re.sub('-', ' ', x)) == re.sub('\s+', ' ', re.sub('-', ' ', n)):
                return n
            if x == n.replace('יי', 'י') or n == x.replace('יי', 'י'):
                return n
            if x == n.replace('וו', 'ו') or n == x.replace('וו', 'ו'):
                return n
        return None

to_match['close_string'] = to_match['yishuv_name'].apply(close_strings)

more_matches = pd.merge(to_match[~to_match["close_string"].isna()], raw_df, how='inner',left_on='close_string', right_on='yishuv_name')
more_matches = more_matches[['yishuv_code', 'yishuv_name_y', 'region_code', 'region', 'local_council_code', 'local_council']]

to_match = to_match[to_match['close_string'].isna()]

to_match.to_excel(r"../Resources/to_match.xlsx")

yishuv_df['match_yishuv'] = yishuv_df['yishuv'].apply(lambda x: dl.get_close_matches(x, raw_df['yishuv_name'])[0])
yishuv_df['yishuv'].apply(lambda x: dl.get_close_matches(x, raw_df['yishuv_name']))
#works, not working with [:2464]
yishuv_df['yishuv'].apply(lambda x: dl.get_close_matches(x, raw_df['yishuv_name'].to_list()[:100]))

yishuv_df['yishuv_match']=yishuv_df['yishuv'].apply(lambda x: raw_df[raw_df['yishuv_name'].str.startswith(x, na=False)]['yishuv_name'].values[0])
raw_df[raw_df['yishuv_name'].str.startswith('שומרי', na=False)==True]