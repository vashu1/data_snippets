# pip install pycurl
# pip install pexpect --upgrade

import json
import pycurl
from StringIO import StringIO
from pexpect import pxssh
import sys
from sshtunnel import SSHTunnelForwarder

club = sys.argv[1]

def download_file_through_jumphost(host, port, url):
    tunnel = SSHTunnelForwarder(
        'jumphost-01.staging.mayhem.arbor.net',
        ssh_username="",
        ssh_pkey="/var/ssh/rsa_key",
        ssh_private_key_password="secret",
        remote_bind_address=(host, port)
    )
    tunnel.start()
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.PORT, tunnel.local_bind_port)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    tunnel.stop()
    data = buffer.getvalue()
    buffer.close()
    return data

def curl_get_json(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    buffer = StringIO()
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    return json.loads(body)

def club_requests(club):
    js = curl_get_json('http://singularity.staging.mayhem.arbor.net/singularity/api/requests/?')
    return [x['request']['id'] for x in js if x['request']['id'].startswith(club + '-')]

for request in club_requests(club):
    print 'Processing {}...'.format(request)
    url = 'http://singularity.staging.mayhem.arbor.net/singularity/api/history/request/{}/tasks/active'.format(request)
    active_tasks = curl_get_json(url)
    if not active_tasks:
        continue

    print "Hosts:"
    for task in active_tasks:
        print task['taskId']['host']
        id = task['taskId']['id']
        js = curl_get_json('http://singularity.staging.mayhem.arbor.net/singularity/api/history/task/{}'.format(id))
        hostname = js['task']['offer']['url']['address']['hostname']
        port = js['task']['offer']['url']['address']['port']
        std_log_url = 'http://0.0.0.0/files/download.json?path={}/stdout'.format(js['directory'])
        print hostname, port, std_log_url
        data = download_file_through_jumphost(hostname, port, std_log_url)
        print len(data)
        f = open(id, 'w')
        f.write(data)
        f.close()

