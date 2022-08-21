import glob
from bs4 import BeautifulSoup
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
import matplotx
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

"""TODO
add comment-page
 <description><![CDATA[В ответ на &lt;a href=&quot;https://www.popadancev.net/istoriya-uslovij-zhizni-chast-2/comment-page-1/#comment-126121&quot;&gt;vashu1&lt;/a&gt;.

furfurol-i-furanovye-smoly/index.html
"""
post_dates = {}
post_authors = {}
comments = []  # author date time postname


def parse_dt(s):
    if ' at ' in s:
        return datetime.datetime.strptime(s, '%d.%m.%Y at %H:%M')
    else:
        return datetime.datetime.strptime(s, '%d %B, %Y')


def post_extract(filename):
    post_name = filename.split('/')[0]
    with open(filename) as f:
        lines = f.readlines()
    page_content = ''.join(lines)
    soup = BeautifulSoup(page_content, 'html.parser')
    footer = soup.find('div', attrs={'class': 'post-footer'})
    if footer:
        dt, author, *_ = footer.text.split('|')
        post_dt = parse_dt(dt.strip())
        post_author = author.split(':')[1].strip()
        post_dates[post_name] = post_dt
        post_authors[post_name] = post_author
    for div_author, div_meta in zip(soup.findAll('div', attrs={'class': 'comment-author'}), soup.findAll('div', attrs={'class': 'comment-meta'})):
        author = div_author.find('span', attrs={'class': 'authorname'}).text
        dt = parse_dt([x for x in div_meta.text.split('\n') if ' at ' in x][0].strip())
        comments.append({'post_name':post_name, 'dt':dt, 'author':author})


# post date   author
# comment - author and datetime

"""
time of day
day of week
author of post and comment records
year posts and comments
month graph?

comment count per post or author - pareto

"""

filenames = []
post_count = 0
for filename in glob.iglob('**/**html**', recursive=True):
    if '/feed/' in filename:
        continue
    if '/comment-page' in filename:
        continue
    if filename.startswith('tag/'):
        continue
    if filename.startswith('sample-page/'):
        continue
    if filename.startswith('wp-json/'):
        continue
    if filename.startswith('feed/'):
        continue
    if filename.startswith('comments/'):
        continue
    if filename.startswith('page/'):
        continue
    if filename.startswith('index.'):
        continue
    if filename.startswith('author/'):
        continue
    if filename.startswith('category/'):
        continue
    if filename.startswith('20') and filename[4] == '/':
        continue
    if filename.startswith('forum/'):
        continue
    filenames.append(filename)
    post_count += 1
    v = len(comments)
    post_extract(filename)
    print(len(comments) - v, post_count, filename)



# kompyuternye-igry
# rele-2
len([x for x in comments if x['post_name'] == 'vosstanovlenie-metricheskoj-sistemy'])
len([x for x in comments if x['post_name'] == 'kompyuternye-igry'])
len([x for x in comments if x['post_name'] == 'rele-2'])
len([x for x in comments if x['post_name'] == 'gatling'])
[i for i in post_authors if 'gatl' in i]

# weekdays
Counter([i['dt'].weekday() for i in comments])
# hour
Counter([i['dt'].time().hour for i in comments])

f = set()
for fn in filenames:
    post_name = fn.split('/')[0]
    f.add(post_name)

f2 = set()
for fn in filenames:
    if fn != (post_name+'/index.html'):
        continue
    post_name = fn.split('/')[0]
    f2.add(post_name)

f - f2


def plot(*args, first_n = None):
    plt.figure()
    for ps in args:
        # ps.sort(reverse=True)
        if first_n:
            ps = ps[:first_n]
        x = range(len(ps))
        y = list(reversed(sorted(ps)))
        plt.plot(x, y)
    plt.show()

all = Counter()
authors0 = Counter()
authors = defaultdict(Counter)
for c in comments:
    a = c['author']
    d = c['dt']
    d = d.split(' at ')[0].split('.')[-1]
    authors[a][d] += 1
    all[d] += 1

#plt.figure()
for a in authors:
    years, cnts = zip(*sorted(authors[a].most_common(), key=lambda v: v[0]))
    years = [int(y) for y in years]
    authors0[a] = sum(cnts)
    if sum(cnts) > 500:
        print(a, years, cnts)
        plt.plot(years, cnts, label=a)

matplotx.line_labels()
plt.show()

a = Counter()
for i in post_authors:
    a[post_authors[i]] += 1

a.most_common()

for i, c in authors0.most_common():
    if 'ash' in i:
        print(i, c)
    if '4e' in i:
        print(i, c)


