"""
Preprocess popodancev.net mirror site files after wget.

# wget --mirror --page-requisites --reject-regex=.*reply.* https://www.popadancev.net
# s3:::popadancev.net http://popadancev.net.s3-website-us-east-1.amazonaws.com

wget --mirror --page-requisites --reject-regex=.*reply.* https://www.popadancev.net
mv www.popadancev.net www.popadancev.net_1
wget --mirror --page-requisites --reject-regex=.*reply.* https://www.popadancev.net
mv www.popadancev.net www.popadancev.net_2
wget --mirror --page-requisites --reject-regex=.*reply.* https://www.popadancev.net
mv www.popadancev.net www.popadancev.net_3

rm -rf merge
cp -R www.popadancev.net_1 merge
rsync -a www.popadancev.net_2/ merge/
rsync -a www.popadancev.net_3/ merge/
cd merge
rm index.html?p=*
rm -rf wp-json/oembed/1.0
rm .DS_Store

# ? rm index_html_p*
# aws s3 cp ./ s3://popadancev.net/ --recursive --profile root
"""
import glob
import os
import re
from bs4 import BeautifulSoup

SITE = 'http://popadancev.net.s3-website-us-east-1.amazonaws.com'


def clean_special_chars(txt):
    txt = txt.replace('/?', '/index_html?')
    for ch in '.?&=':
        txt = txt.replace(ch, '_')
    if txt.endswith('_html'):
        txt = txt[:-5] + '.html'
    else:
        if not txt.endswith('/'):
            txt += '.html'
    return txt


def clean_href(txt, start="href='", end="'"):
    position = txt.find(start)
    while position >= 0:
        s = position + len(start)
        e = txt.find(end, s)
        url = txt[s:e]
        if 'popadancev' in url:
            new_url = clean_special_chars(url)
            new_url = new_url.replace('amp;', '')
            if url != new_url:
                txt = txt.replace(url, new_url)
        position = txt.find(start, position + len(start))
    return txt


def drop_dynamic_elements(lines):
    page_content = ''.join(lines)
    soup = BeautifulSoup(page_content, 'html.parser')
    search_form = soup.find('form', attrs={'class': 'searchform'})
    if search_form:
        search_form.decompose()
    else:
        print('no search_form')
    comment_respond = soup.find('div', attrs={'class': 'comment-respond'})
    if comment_respond:
        comment_respond.decompose()
    else:
        print('no comment_respond')
    return [(line + '\n') for line in str(soup).split('\n')]


def fix_comment_anchors(line):
    return re.sub(r'#comment-([0-9]*).html', r'#comment-\1', line)


def fix_file(filename):
    with open(filename) as f:
        lines = f.readlines()


lines = drop_dynamic_elements(lines)
if clean_special_chars(filename) != filename:
    os.remove(filename)
    filename = clean_special_chars(filename)
for i in range(len(lines)):
    lines[i] = clean_href(lines[i], start="href='", end="'")
    lines[i] = clean_href(lines[i], start='href="', end='"')
    lines[i] = lines[i].replace('https://www_popadancev_net', SITE)
    lines[i] = lines[i].replace('https://popadancev_net', SITE)
    lines[i] = lines[i].replace('http://popadancev_net', SITE)
    lines[i] = lines[i].replace('http://www_popadancev_net', SITE)
    lines[i] = lines[i].replace('www.popadancev.net', SITE)
    lines[i] = lines[i].replace('https://popadancev.net', SITE)
    lines[i] = lines[i].replace('http://popadancev.net/', SITE + '/')
    lines[i] = lines[i].replace('www.popadancev.net', SITE)
    lines[i] = lines[i].replace('http://http://', 'http://')
    lines[i] = lines[i].replace('https://http//', 'http://')
    lines[i] = lines[i].replace('https://http://', 'http://')
    lines[i] = fix_comment_anchors(lines[i])
with open(filename, 'w') as f:
    for line in lines:
        _ = f.write(line)

for filename in glob.iglob('**/**html**', recursive=True):
    print(filename)
    fix_file(filename)
