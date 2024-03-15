import sys
from internetarchive import get_session, get_item, get_files

video_file_types = {'Matroska', 'WebM', 'MPEG4'}
thumb_file_types = {'JPEG', 'WebP', 'Thumbnail'}
info_file_types = {'JSON'}

f = open('upload_issues.txt', 'w')

EMAIL = ''

s = get_session()
s.mount_http_adapter()
search_results = s.search_items(f'uploader:{EMAIL}', fields=['identifier', 'format'])
for result in search_results:
    contains_video = False
    contains_info = False
    contains_thumb = False

    id = result['identifier']
    files = set(result['format'])
    if video_file_types & files:
        contains_video = True
    if thumb_file_types & files:
        contains_thumb = True
    if info_file_types & files:
        contains_info = True

    # print(result['identifier'])
    # print(result['format'])
    
    if (contains_video and contains_thumb and contains_info) == False:
        missing = 'Missing: ' + ("" if contains_video else "Video,") + ("" if contains_thumb else "Thumbnail,") + ("" if contains_info else "info.json")
        f.write(id + '\t  [' + ', '.join(result['format']) + ']\t\t' + missing + '\n')
        
f.close()
