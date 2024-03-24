EMAIL = ''
SKIP_THUMBNAIL_CHECK = True
IS_ROOSTER = True

import sys
from internetarchive import get_session

video_file_types = {'Matroska', 'WebM', 'MPEG4'}
thumb_file_types = {'JPEG', 'WebP', 'PNG', 'Thumbnail'}
info_file_types = {'JSON'}


if EMAIL == '':
    print('Please enter your email on line 1')
    sys.exit(1)

f = open('upload_issues.txt', 'w')
f2 = open('incomplete_original_urls.txt', 'w')
f3 = open('incomplete_archive_urls.txt', 'w')

s = get_session()
s.mount_http_adapter()

search_results = s.search_items(f'uploader:({EMAIL})', fields=['identifier', 'format', 'originalurl'])
for result in search_results:
    contains_video = False
    contains_info = False
    contains_thumb = False

    id: str = result['identifier']
    # Skip uploads that aren't from tubeup
    if IS_ROOSTER and not id.startswith('roosterteeth-'):
        continue
    elif not IS_ROOSTER and not id.startswith('youtube-'):
        continue

    original_url: str = result['originalurl']

    files = set(result['format'])
    if video_file_types & files:
        contains_video = True
    if (thumb_file_types & files) or SKIP_THUMBNAIL_CHECK:
        contains_thumb = True
    if info_file_types & files:
        contains_info = True
    
    if (contains_video and contains_thumb and contains_info) == False:
        missing = 'Missing: ' + ("" if contains_video else "Video,") + ("" if contains_thumb else "Thumbnail,") + ("" if contains_info else "info.json")
        f.write(id + '\t  [' + ', '.join(result['format']) + ']\t\t' + missing + '\n')
        
        if IS_ROOSTER:
            f2.write(original_url + '\n')
            f3.write(f"https://archive.org/details/{id}" + '\n')
        else:
            youtube_id = id.removeprefix('youtube-')
            youtube_url = 'https://www.youtube.com/watch?v=' + youtube_id
            f2.write(youtube_url + '\n')
            f3.write(f"https://archive.org/details/{id}" + '\n')

f.close()
f2.close()
f3.close()
