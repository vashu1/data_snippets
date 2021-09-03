"""
Setup IMAP access in Yandex mail.
https://mail.yandex.com/
Все настройки -> Прочие -> Почтовые программы ->
tick С сервера imap.yandex.ru по протоколу IMAP
tick Пароли приложений и OAuth-токены
?tick Отключить автоматическое удаление писем, помеченных в IMAP как удаленные

https://passport.yandex.com/profile/
Passwords and authorization -> App passwords

# counts
# by weekday
cat data.txt | awk '{print $4;}' | sort | uniq -c
# by author
cat data.txt | awk '{print $5;}' | sort | uniq -c | sort -g
"""
import base64
from imaplib import IMAP4_SSL
from datetime import datetime
import getpass

LJ_MAIL_FOLDER = 'livejournal'

with IMAP4_SSL("imap.yandex.ru") as M, open('data.txt', 'w') as f:
    print('Input email:')
    email = input()
    M.login(email, getpass.getpass())
    M.select(LJ_MAIL_FOLDER)
    typ, data = M.search(None, 'ALL')
    msg_ids = data[0].split()
    for indx, num in enumerate(msg_ids):
        typ, data = M.fetch(num, '(RFC822)')
        msg = data[0][1].decode()
        msg = msg.split('\r\n')
        dt = list(filter(lambda line: line.startswith('Date: '), msg))[0]
        dt = datetime.strptime(dt, 'Date:  %a, %d %b %Y %H:%M:%S %z')
        subject = list(filter(lambda line: line.startswith('Subject: '), msg))[0]
        if 'UTF' not in subject:
            print(f'{indx} SKIP:', subject)
            continue
        subject = subject.replace('Subject: =?UTF-8?B?', '')
        subject = base64.b64decode(subject).decode()
        if 'обновил' not in subject:
            print(f'{indx} SKIP:', subject)
            continue
        result = f'{dt.year} {dt.month} {dt.day} {dt.weekday()} {subject.split(" ")[0]}'
        print(f'{indx} SAVE:', result)
        _ = f.write(result + '\n')