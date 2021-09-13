import shelve

with shelve.open('state') as db:
    print('HITId:', db['HITId'])
    print('workers')
    for i in db['workers']:
        print(i)
    print('accepted')
    for i in db['accepted']:
        print(i['Answer'])