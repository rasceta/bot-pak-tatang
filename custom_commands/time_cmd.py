import pytz
from pytz import timezone
from datetime import datetime

def get_time_by_city(city):
    base_zone = timezone('UTC')
    city_zone = None
    for x in pytz.all_timezones:
        if str.lower(city) in str.lower(x):
            city_zone = x
    if city_zone is not None:
        your_zone = timezone(city_zone)
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        base_dt = base_zone.localize(datetime.now())
        your_dt = base_dt.astimezone(your_zone)   
        return f'Current time in {city_zone} : {str(your_dt.strftime(fmt))}'
    else:
        return 'Your city is not registered in current list'