#Created: Thu May 23 01:20:51 2019
#By: mach

from datetime import datetime

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