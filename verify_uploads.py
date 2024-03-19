EMAIL = 'kevin.farmer96@gmail.com'
SKIP_THUMBNAIL_CHECK = True
IS_ROOSTER = False

import sys
from internetarchive import get_session

video_file_types = {'Matroska', 'WebM', 'MPEG4'}
thumb_file_types = {'JPEG', 'WebP', 'Thumbnail'}
info_file_types = {'JSON'}

if EMAIL == '':
    print('Please enter your email on line 1')
    sys.exit(1)

f = open('upload_issues.txt', 'w')
f2 = open('problem_ids.txt', 'w')

s = get_session()
s.mount_http_adapter()
search_results = s.search_items(f'uploader:{EMAIL}', fields=['identifier', 'format'])
for result in search_results:
    contains_video = False
    contains_info = False
    contains_thumb = False

    id: str = result['identifier']
    # Skip uploads that aren't from tubeup
    if IS_ROOSTER and not id.startswith('roosterteeth-'):
        continue
    elif not id.startswith('youtube-'):
        continue

    files = set(result['format'])
    if video_file_types & files:
        contains_video = True
    if (thumb_file_types & files) or SKIP_THUMBNAIL_CHECK:
        contains_thumb = True
    if info_file_types & files:
        contains_info = True

    # print(result['identifier'])
    # print(result['format'])
    
    if (contains_video and contains_thumb and contains_info) == False:
        if not IS_ROOSTER:
            missing = 'Missing: ' + ("" if contains_video else "Video,") + ("" if contains_thumb else "Thumbnail,") + ("" if contains_info else "info.json")
            f.write(id + '\t  [' + ', '.join(result['format']) + ']\t\t' + missing + '\n')
        
        if IS_ROOSTER:
            f2.write(id + '\n')
        else:
            youtube_id = id.removeprefix('youtube-')
            youtube_url = 'https://www.youtube.com/watch?v=' + youtube_id
            f2.write(youtube_url + '\n')

f.close()
f2.close()
