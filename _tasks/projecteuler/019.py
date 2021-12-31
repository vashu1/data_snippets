
from datetime import timedelta, date

# how many Sundays between dates

start = date(1901, 1, 1)
end = date(2000, 12, 31)

while start.weekday() != 6:
    start += timedelta(days=1)

sunday_count = (end - start).days // 7 + 1

print(sunday_count)

# iterative

start = date(1901, 1, 1)
end = date(2000, 12, 31)

count = 0
while True:
    if start.weekday() == 6:
        count += 1
    start += timedelta(days=1)
    if start > end:
        print(start)
        print(count)
        break

# How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

start = date(1901, 1, 1)
end = date(2000, 12, 31)

count = 0
while True:
    if start.weekday() == 6 and start.day == 1:
        count += 1
    start += timedelta(days=1)
    if start > end:
        print(start)
        print(count)
        break
