import pandas as pd
import numpy as np
import datetime as dt

#SOME USEFUL FUNCTIONS
def date_to_nth_day(date, format='%Y-%m-%d'):
    """converts full date date to nth day in the year"""
    date = pd.to_datetime(date, format=format)
    new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
    return (date - new_year_day).days + 1

def nth_day_to_date(nth, year, format='%Y-%m-%d'):
    """returns a full date, given the nth day in the year and a year"""
    start = pd.to_datetime(F"{year}-01-01", format=format)
    return (start + dt.timedelta(days=nth-1))

#CREATE A BASE DATAFRAME df
def make_dataframe(stations=["35T","36T","37T"], years=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]):
    dfs = []
    for year in years:
        df = pd.read_excel(F"yearly_data\pm25_2011_2020\PM2.5({year}).xlsx")
        df.columns = [col_name.strip() for col_name in df.columns] #some column names have spaces around
        
        for st in stations: #for each year we want all stations that were specified above
            if st not in df.columns:
                df[st] = np.nan  
                
        if year%4 == 0: #is leap year
            df = df[:366]
        else:
            df = df[:365]
            
        dfs.append(df)
    
    df = pd.concat(dfs, ignore_index=True)
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
    df['nth'] = df['Date'].apply(lambda date: date_to_nth_day(date))
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df.insert(1, 'Year', df.pop('Year'))
    df.insert(2, 'Month', df.pop('Month'))
    df.insert(3, 'nth', df.pop('nth'))

    return df

#make_dataframe().to_excel("pm25_2011_2020.xlsx")
