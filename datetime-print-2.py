import datetime

date_time_str = '2018-06-29T08:15:27.243860-07:00'  
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f%z')

print('Date:', date_time_obj.date())  
print('Time:', date_time_obj.time())  
print('Date-time:', date_time_obj)
print('Date-time str:', date_time_str)
