EMAIL = ''
SKIP_THUMBNAILS = True

from internetarchive import get_session, get_item, get_files

video_file_types = {'Matroska', 'WebM', 'MPEG4'}
thumb_file_types = {'JPEG', 'WebP', 'Thumbnail'}
info_file_types = {'JSON'}

if EMAIL == '':
    print('Please enter your email on line 1')

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
    if not id.startswith('youtube-'):
        continue

    files = set(result['format'])
    if video_file_types & files:
        contains_video = True
    if (thumb_file_types & files) or SKIP_THUMBNAILS:
        contains_thumb = True
    if info_file_types & files:
        contains_info = True

    # print(result['identifier'])
    # print(result['format'])
    
    if (contains_video and contains_thumb and contains_info) == False:
        missing = 'Missing: ' + ("" if contains_video else "Video,") + ("" if contains_thumb else "Thumbnail,") + ("" if contains_info else "info.json")
        f.write(id + '\t  [' + ', '.join(result['format']) + ']\t\t' + missing + '\n')
        
        youtube_id = id.removeprefix('youtube-')
        youtube_url = 'https://www.youtube.com/watch?v=' + youtube_id
        f2.write(youtube_url + '\n')

f.close()
