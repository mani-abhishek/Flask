from datetime import date,datetime


print(datetime.now())

print(datetime.today().replace(microsecond=0))

date_format = "%Y-%m-%d %H:%M:%S"
a = datetime.strptime('2022-07-18 08:23:10', date_format)
b = datetime.strptime(str(datetime.today().replace(microsecond=0)), date_format)
delta = b - a
print(delta.days)
print(delta.seconds)