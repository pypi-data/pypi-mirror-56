#Meteorological Analysis functions

from datetime import datetime
import time

def day_to_date(year,jday):
    start = datetime(year-1,12,31,0,0).toordinal()
    temp_day = int(jday)
    month = datetime.fromordinal(start+temp_day)
    day = month.day
    month = month.month
    hour = int((jday - temp_day)*24)
    minute = int((jday - temp_day - hour/24)*24*60)
    second = int((jday - temp_day - hour/24 - minute/(24*60))*24*60*60)
    microsecond = int((jday - temp_day - hour/24 - minute/(24*60) - second/(24*60*60))*24*60*60*1000)
    return datetime(year, month, day, hour, minute, second, microsecond)

def min_to_hour_min(t):
    st = []
    for i in range(0,t.size):
        st.append(time.strftime('%H:%M',time.gmtime(t[i])))
    return st

def day_to_seconds(jday):
    second = jday * 24 * 60 * 60
    return second