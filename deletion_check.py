URL_FILE = './AH_Archival_Problem_links.txt'

import sys, time
from internetarchive import get_session
import requests


if URL_FILE == '':
    print('Please enter a path to your ID file on line 1')
    sys.exit(1)

file_name = URL_FILE.split('/')[-1].removesuffix('.txt')

s = get_session()
s.mount_http_adapter()

input_file = open(URL_FILE, 'r')
missing_id_file = open(f'{file_name}_deletion_check_missing_ids.txt', 'w')
deleted_id_file = open(f'{file_name}_deletion_check_deleted_ids.txt', 'w')

contents = input_file.read()
lines = contents.split('\n')
urls = [line for line in lines if line.startswith('https://archive.org/details/')  ]

size = len(urls)
for i, url in enumerate(urls):
    print(f"Checking {url}\t({i+1}/{size})")
    res = requests.get(url)
    is_deleted = ('This item is no longer available' in res.text)

    if is_deleted:
        # print(f"Is deleted: {url}")
        deleted_id_file.write(url + "\n")
    else:
        # print(f"Is missing: {url}")
        missing_id_file.write(url + "\n")

    time.sleep(0.1)

input_file.close()
missing_id_file.close()
deleted_id_file.close()
