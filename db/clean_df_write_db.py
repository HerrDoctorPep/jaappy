#!/usr/bin/env python

""" 
WRITING HOUSES TO DATABASE

Leverage existing cleaning and filtering code from Start_Modelling.ipynb

By: dr.Pep

"""
import pandas as pd
import numpy as np
import re
import os
import logging
import mysql.connector
from sqlalchemy import create_engine, select
from sqlalchemy import Table, MetaData
from datetime import datetime

# Set up logging
LOGDATA = 'data/logs/'
TODAY = date.today().strftime("%Y%m%d") # The current date in the standard format YYYYMMDD
LOGFILE = 'log_'+TODAY+'.txt'
logging.basicConfig(filename = LOGDATA + LOGFILE,
                    level = logging.DEBUG)
logging.info('Running script clean_df_write_db.py | Time stamp: ' + str(time.asctime()))

# DEFINE DATABASE CONNECTION
# Need to define environment variables
# On windows: $env:SQL_USER="xxxxx"
connect_string = 'mysql+mysqlconnector://' + os.environ.get('SQL_USER') +':' + os.environ.get('SQL_WW') + '@192.168.178.30:3306' + '/houses_db'
engine = create_engine(connect_string, echo=False)
logging.info('Database engine: ' + str(engine))

# HERE ARE SOME HELPFUL FUNCTIONS
# Still need to add logging to allow debugging when live

def sql_date(file_name):
    file_date = re.findall('\d+',file_name)[0]
    sql_dt = file_date[0:4] + "-" + file_date[4:6] + "-" + file_date[6:8]
    return sql_dt

def check_is_in_table(file_name):
    connection = engine.connect()
    sql_date(file_name)
    
    metadata = MetaData()
    houses_detail_tbl = Table('houses_detail', metadata, autoload = True, autoload_with=engine)
    query = select([
        houses_detail_tbl.columns.ScrapeDate]
        ).where(
            houses_detail_tbl.columns.ScrapeDate == sql_date(file_name)
            )

    results = connection.execute(query).first()
    return (results != None)

def fix_missing_values(df):
    # Zip via address
    zeros_fixable = df[df['Zip'].isnull()].index 
    df.loc[zeros_fixable,'Zip'] = df.loc[zeros_fixable,'Address'].apply(
                lambda x: x.split(',')[1].strip()
                )    
 
    # Kamers via  Slaapkamers
    zeros_fixable = df[(df['Kamers'].isnull() == True) 
        & (df['Slaapkamers'].isnull() ==False)].index
    df.loc[
        zeros_fixable,'Kamers'] = 1 + df.loc[zeros_fixable,'Slaapkamers'] 
    
    # k.k. most common Pricetype
    zeros_fixable = df[df['Pricetype'].isnull()].index 
    df.loc[zeros_fixable,'Pricetype'] = 'k.k.'

    # Perceeloppervlakte 0 als ontbrekend
    zeros_fixable = df[df['Perceeloppervlakte'].isnull()].index 
    df.loc[zeros_fixable,'Perceeloppervlakte'] = 0 # put zero where not applicable   
    
    return df

def drop_missing_values(df):
    # Vraagprijs, Kamers, Bouwjaar, ZipCode, Lat/Lon all necessary
    zeros_not_fixable = df  [
        df['Huidige_vraagprijs'].isnull()
        | df['Kamers'].isnull()
        | df['ZipCode'].isnull()
        | df['Latitude'].isnull()
        | df['Longitude'].isnull()
        | df['Bouwjaar'].isnull()].index
    
    df = df.drop(zeros_not_fixable)
    
    return df

def Zip_get_latlon(zip_code):
    Zip_geo = pd.read_csv("data/processed/postcode_roffa_geo.csv",index_col = "PostCode")
    try:
        lat = Zip_geo.loc[zip_code]['latitude']
        lon = Zip_geo.loc[zip_code]['longitude']
    except:
        lat = None
        lon = None
    return [lat,lon]

def read_and_clean(file_name):
    df_houses_detail = fix_missing_values(pd.read_csv(os.path.join('data/processed/', file_name)))

    df_houses_detail['ScrapeDate'] = datetime.strptime(sql_date(file_name), '%Y-%m-%d').date()
            
    df_houses_detail['ZipCode'] = (df_houses_detail['Zip'].str.extract(
        "([0-9]+ [A-Z][A-Z])", expand = True))
    df_houses_detail['ZipCode'] = df_houses_detail['ZipCode'].str.replace(' ','')

    df_houses_detail['Latitude'] = df_houses_detail['ZipCode'].apply(lambda x: Zip_get_latlon(x)[0])
    df_houses_detail['Longitude'] = df_houses_detail['ZipCode'].apply(lambda x: Zip_get_latlon(x)[1])

    df_houses_detail = drop_missing_values(df_houses_detail)

    df_houses_detail['Huidige_vraagprijs_per_m2'] = df_houses_detail['Huidige_vraagprijs'] / df_houses_detail['Woonoppervlakte']

    df_houses_detail.rename(columns = {'Energielabel_(geschat)':'Energielabel'}, inplace = True)
    df_houses_detail.rename(columns = {'Energieverbruik_(geschat)':'Energieverbruik'}, inplace = True)

    return df_houses_detail

def main():
    # For now only do one file (easy to substitute for whole folder)
    file_list = os.listdir('data/processed/')

    # file_list=['houses_detail_20210206.csv']

    for file in file_list:
        if (file.startswith("houses_detail_") & file.endswith(".csv")):
            if (not check_is_in_table(file)):
                logging.info("File " + file + " is not yet in the database")
                try:
                    df_houses_detail = read_and_clean(file)
                    logging.info("File " + file + " has been pre-processed")
                except:
                    logging.error("File " + file + " could not be pre-processed")
                try:
                    df_houses_detail.to_sql(
                        'houses_detail', 
                        con=engine, 
                        if_exists='append'
                        )
                    logging.info("File " + file + " has been added to the database")
                except:
                    logging.error("File " + file + " could not be added to the database")
            else: 
                logging.warning("File " + file + " is ignored: Scrapedate already occurs in table")
        else:
            logging.warning("File " + file + " is ignored: Filename format is incorrect")

if __name__ == "__main__":
    main()