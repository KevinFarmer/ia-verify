import re, json
from pytube import Channel, Playlist

# Note: have to manually apply this PR to your local version of pytube to handle @username channels correctly:
# https://github.com/pytube/pytube/pull/1444/commits/84eccec80f589f0f759f4b4d11e03ee0220efca4

def process_playlist(playlist_id):
    playlist_url = f'https://www.youtube.com/playlist?list={playlist_id}'

    playlist = Playlist(playlist_url)
    print('Playlist: ' + playlist.title)
    

    playlist_info = {}
    playlist_info['title'] = playlist.title
    playlist_info['owner'] = playlist.owner
    playlist_info['owner_url'] = playlist.owner_url

    # TODO sort videos / reverse order if 1st item is the latest
    playlist_videos = playlist.videos
    print('Number Of Videos In playlist: %s' % len(playlist_videos))
    videos = []
    for vid in playlist_videos:
        video = {
            "video_id": vid.video_id,
            "title": vid.title,
            "url": f"https://archive.org/details/youtube-{vid.video_id}"
        }
        videos.append(video)
    playlist_info['videos'] = videos

    return playlist_info


def get_playlist_ids(playlist_html):
    matches: list[str] = re.findall('\"playlistId\":\".+?(?=\")', playlist_html)
    playlist_ids = [m.replace('"', '').split(':')[-1] for m in matches]
    playlist_ids = list(set(playlist_ids))
    playlist_ids.sort()
    return playlist_ids



input_file = open('./channels_with_playlists.txt', 'r')

contents = input_file.read()
channel_urls = contents.split('\n')
channel_urls.remove('')

playlists_output = []
for url in channel_urls:
    print(url)
    c = Channel(url)
    channel_name = c.channel_name
    print(f"Channel: {channel_name}")
    channel_dict = {}
    channel_dict['channel_name'] = channel_name

    # TODO sort playlists by name
    playlist_ids = get_playlist_ids(c.playlists_html)
    channel_playlists = []
    for playlist_id in playlist_ids:
        playlist_info = process_playlist(playlist_id)
        channel_playlists.append(playlist_info)

    channel_dict['playlists'] = channel_playlists
    playlists_output.append(channel_dict)

with open('playlist_output_v2.json', 'w') as outfile:
    json.dump(playlists_output, outfile)

input_file.close()
