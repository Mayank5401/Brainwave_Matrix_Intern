import datetime as dt
ts = "2023-02-01 12:30:45"
dt_obj = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
print(dt_obj)