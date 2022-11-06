import requests
#from datetime import date, timedelta
import pandas as pd
import pymysql
import sqlalchemy
import argparse

# def get_last_date_from_sql_table():
#     db = pymysql.connect(host=host, port=port, user=user)
#     cur = db.cursor(pymysql.cursors.DictCursor)
#     cur.execute("SELECT ParentGuardianID FROM ParentGuardianInformation WHERE UserID ='" + UserID + "'"))

def get_expost_data_from_noga(start_dt, end_dt):
    start_dt= start_dt.strftime("%d/%m/%Y")
    end_dt = end_dt.strftime("%d/%m/%Y")
    #today = date.today()
    #end_dt = today.strftime("%d/%m/%Y")
    # need to change the start_dt to be the last record date in the database
    #n_days_ago = 5
    #start_dt = today - timedelta(days=n_days_ago)
    start_dt = start_dt.strftime("%d/%m/%Y")
    api_url = 'https://www.noga-iso.co.il/Umbraco/Api/Documents/GetCosts/?startDateString='+start_dt+'&endDateString='+end_dt+'&culture=he-IL&dataType=Cost'
    #api_url = "https://www.noga-iso.co.il/Umbraco/Api/Documents/GetCosts/?startDateString=01/08/2022&endDateString=31/08/2022&culture=he-IL&dataType=Cost"
    response = requests.get(api_url)
    return response.json()

if __name__ == '__main__':
    res = get_expost_data_from_noga('01/09/2022', '30/09/2022')
    df = pd.DataFrame.from_dict(res)
    df = df.drop_duplicates()
    df = df.rename(columns={"Index":"id", "Date":"rec_date", "Time":"rec_time", "Cost":"cost", "RenewableGen":"renewable_gen",
                          "ConventionalGen":"conventional_gen", "SystemDemand":"system_demand"  })
    df = df.loc[:, df.columns != 'id']
    print(df.groupby([pd.DatetimeIndex(df['rec_date']).year,pd.DatetimeIndex(df['rec_date']).month]).size())

    parser = argparse.ArgumentParser(description='Use your username and password to connect to MySQL')
    parser.add_argument("user", help="your MySQL username")
    parser.add_argument("pwd", help="your MySQL password")
    #parser.add_argument("port", type=int, default=3306, help="your MySQL port")
    parser.add_argument("tablename", help="The table name to which you want to append the data")
    parser.add_argument("database", default='nzo_db', help="The database to which you want to connect")
    parser.add_argument("host", default='localhost', help="your MySQL host")
    args = parser.parse_args()
    database_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(args.user, args.pwd, args.host, args.databases))
    df.to_sql(con=database_connection, name=args.tablename, if_exists='append', index=False)

#noga_expost_data_raw
##database_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, passw, host, database))


##create_query = "CREATE TABLE noga_expost_data (id INT NOT NULL AUTO_INCREMENT, rec_date date NOT NULL, rec_time time NOT NULL, " \
##               "cost double NOT NULL, renewable_gen double NOT NULL, conventional_gen double NOT NULL, system_demand double NOT NULL, PRIMARY KEY (id));"

# parse and write the results to the data base

# validation for the data:
# remove duplications
# check that each day has 48 records
# check that each month has data for all the days
# send a report with the results of the validations