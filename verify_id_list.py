ID_FILE = './AllChannels.txt'
SKIP_THUMBNAIL_CHECK = True
CHUNK_SIZE = 250

import sys
from internetarchive import get_session

video_file_types = {'Matroska', 'WebM', 'MPEG4'}
thumb_file_types = {'JPEG', 'WebP', 'Thumbnail'}
info_file_types = {'JSON'}

if ID_FILE == '':
    print('Please enter a path to your ID file on line 1')
    sys.exit(1)

file_name = ID_FILE.split('/')[-1].removesuffix('.txt')

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


s = get_session()
s.mount_http_adapter()

input_file = open(ID_FILE, 'r')
missing_id_file = open(f'{file_name}_missing_ids_from_list.txt', 'w')
problem_id_file = open(f'{file_name}_problem_ids_from_list.txt', 'w')

contents = input_file.read()
lines = contents.split('\n')
ids = [line.removeprefix('https://www.youtube.com/watch?v=') for line in lines]
ids = [id.removeprefix('https://www.youtube.com/shorts/') for id in ids]
ids = [id for id in ids if id != '']
ids = [f"youtube-{id}" for id in ids]


id_chunks = list(chunks(ids, CHUNK_SIZE))

num = len(id_chunks)
for i, id_list in enumerate(id_chunks):
    id_search = ' OR '.join(id_list)

    search_results = s.search_items(f'identifier:({id_search})', fields=['identifier', 'format'])
    found_ids = [result['identifier'] for result in search_results]
    missing_ids = list(set(id_list) - set(found_ids))
    if len(missing_ids) > 0:
        missing_ids_output = "\n".join(missing_ids) + "\n"
        missing_id_file.write(missing_ids_output)

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
        if (thumb_file_types & files) or SKIP_THUMBNAIL_CHECK:
            contains_thumb = True
        if info_file_types & files:
            contains_info = True

        if (contains_video and contains_thumb and contains_info) == False:
            youtube_id = id.removeprefix('youtube-')
            youtube_url = 'https://www.youtube.com/watch?v=' + youtube_id
            problem_id_file.write(youtube_url + '\n')
    print(f"Finished batch {i} / {num}")

input_file.close()
missing_id_file.close()
problem_id_file.close()
