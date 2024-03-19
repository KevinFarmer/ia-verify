
# for single channel
# yt-dlp --flat-playlist --print "%(playlist_uploader_id)s,https://www.youtube.com/playlist?list=%(id)s" "https://www.youtube.com/@AchievementHunter/playlists"

# New version
Write-Output "" > "playlist_output.txt"
Get-Content -Path ".\channels_with_playlists.txt" | ForEach-Object {
    Write-Output "$_"
    $playlist_url = "$_" + "/playlists"
    yt-dlp --flat-playlist --print "%(playlist_uploader_id)s,https://www.youtube.com/playlist?list=%(id)s" "$playlist_url" >> "playlist_output.txt"
}
