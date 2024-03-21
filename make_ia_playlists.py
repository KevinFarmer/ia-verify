import re, json
from datetime import datetime
import requests
from pytube import Channel, Playlist, YouTube

# Note: have to manually apply this PR to your local version of pytube to handle @username channels correctly:
# https://github.com/pytube/pytube/pull/1444/commits/84eccec80f589f0f759f4b4d11e03ee0220efca4


# If more than one videos is missing, put them in the CORRECT ORDER and use the desired ending index for each
missing_videos = {
    'https://www.youtube.com/playlist?list=PL1cXh4tWqmsH3L0vKNfqLgJj6KAPIRUPi': [
        {
            'video_id': 'RB5TBmqrJvo',
            'playlist_index': 4 # Starting from 1, not 0
        }
    ]
}

def process_playlist(playlist_url: str):
    # playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'
    playlist = Playlist(playlist_url)
    print('Playlist: ' + playlist.title)

    playlist_id = playlist_url.removeprefix('https://www.youtube.com/playlist?list=')

    playlist_info = {}
    playlist_info['playlist_id'] = playlist_id
    playlist_info['title'] = playlist.title
    playlist_info['owner'] = playlist.owner
    playlist_info['owner_url'] = playlist.owner_url


    playlist_videos = playlist.videos
    print('Number Of Videos In playlist: %s' % len(playlist_videos))
   
    playlist_videos = [vid for vid in playlist_videos]
    if playlist_url in missing_videos.keys():
        missing_pl_vids = missing_videos.get(playlist_url)
        for v in missing_pl_vids:
            id = v['video_id']
            index = v['playlist_index'] - 1
            vid = YouTube(f'https://www.youtube.com/watch?v={id}')
            playlist_videos = playlist_videos[0:index] + [vid] + playlist_videos[index:]


    # sort videos / reverse order if 1st item is the latest
    reverse = False
    if len(playlist_videos) > 1:
        first_publish_date = playlist_videos[0].publish_date
        last_publish_date = playlist_videos[-1].publish_date
        if first_publish_date > last_publish_date:
            reverse = True

    videos = []
    for vid in playlist_videos:
        video = {
            "video_id": vid.video_id,
            "title": vid.title,
            "url": f"https://archive.org/details/youtube-{vid.video_id}"
        }
        videos.append(video)

    if reverse:
        videos.reverse()
    playlist_info['videos'] = videos

    return playlist_info


def get_playlist_ids(playlist_html):
    matches: list[str] = re.findall('\"playlistId\":\".+?(?=\")', playlist_html)
    playlist_ids = [m.replace('"', '').split(':')[-1] for m in matches]
    playlist_ids = list(set(playlist_ids))
    playlist_ids.sort()
    return playlist_ids



input_file = open('playlist_input.txt', 'r')
RUN_DOWNLOAD = True

contents = input_file.read()
lines = contents.split('\n')
while '' in lines:
    lines.remove('')

channels_dict = {}
for line in lines:
    channel_id, pl = line.split(',')
    playlists = channels_dict.get(channel_id)
    if playlists is None:
        playlists = []
    playlists.append(pl)
    channels_dict[channel_id] = playlists


# channels_dict = {'@Letsplay': ['https://www.youtube.com/playlist?list=PLbIc1971kgPBpEGgBlafp48ZJ0WHF2ax1']}
if RUN_DOWNLOAD:
    for channel_id, playlists_urls in channels_dict.items():
        print(f"Starting {channel_id} at {datetime.now()}")
        url = f"https://www.youtube.com/{channel_id}"
        c = Channel(url)
        channel_name = c.channel_name
        print(f"Channel: {channel_name}")
        channel_dict = {}
        channel_dict['channel_name'] = channel_name
        channel_dict['channel_id'] = channel_id

        channel_playlists = []
        for playlist_url in playlists_urls:
            playlist_info = process_playlist(playlist_url)
            channel_playlists.append(playlist_info)

        channel_playlists = sorted(channel_playlists, key=lambda x: x['title'])
        channel_dict['playlists'] = channel_playlists
        with open(f'playlists/{channel_id}.json', 'w') as outfile:
            json.dump(channel_dict, outfile, default=str)
        print(f"Completed {channel_id} at {datetime.now()}\n\n\n")

if not RUN_DOWNLOAD:
    playlists_output = []
    for channel_id in channels_dict.keys():
        print(f"Reading {channel_id} file")
        with open(f'playlists/{channel_id}.json', 'r') as infile:
            channel_dict = json.load(infile)
            playlists_output.append(channel_dict)

    playlists_output = sorted(playlists_output, key=lambda x: x['channel_name'])

    output_file = 'playlist_output_v6.json'
    print(f'Writing output to file {output_file}')
    with open(output_file, 'w') as outfile:
        json.dump(playlists_output, outfile, default=str)

input_file.close()
