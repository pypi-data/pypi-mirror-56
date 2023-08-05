import pandas as pd
import sys
from .exceptions import DataSelectorException

def dataset_selector(f):
    def wrapper(*args, **kw):
        try:
            check_values(kw)
            dataframe = kw['dataframe']
            identifier = kw['dataIdentifier']
            selector = kw['selector']
            kw['dataframe'] = select_df(dataframe, selector, identifier)
            del kw['selector']
            return f(*args, **kw)
        except Exception as e:
            raise e
            print(str(e))

    return wrapper

def select_df(df, selector, identifier):
    df = df.copy()
    if pd.api.types.is_numeric_dtype(df[identifier.timestamp]):
        df['date'] = pd.to_datetime(df[identifier.timestamp].astype(int), unit='s')
    else:
        df['date'] = pd.to_datetime(df[identifier.timestamp])
    if((selector.start_date is not None) and (selector.end_date is not None)):
        mask = (df['date'] > selector.start_date) & (df['date'] < selector.end_date)
        df = df.loc[mask]
    if(selector.week_days is not None):
        weekDays = [day for day in range(0, len(selector.week_days)) if selector.week_days[day] == "1"]
        df['weekday'] = df['date'].apply(lambda x: x.weekday())
        df = df[df['weekday'].isin(weekDays)]
    if(selector.day_hours is not None):
        dayHours = [hour for hour in range(0, len(selector.day_hours)) if selector.day_hours[hour] == "1"]
        df['dayHour'] = df['date'].apply(lambda x: x.hour)
        df = df[df['dayHour'].isin(dayHours)]  
    print(df.size)
    return df

def check_values(kw):
    params = ['dataframe', 'dataIdentifier', 'selector']
    for param in params:
        if param not in kw:
            raise DataSelectorException(parameter=param)
    