# TubeUp Usage Tutorial

## Pre-requisite: Complete the [TubeUp Installation Tutorial](https://github.com/KevinFarmer/ia-verify/blob/main/tubeup_install.md)

### Download an input file
To begin, download one or more files with youtube links from the #youtube-channels chat in Discord

Example: ids.txt, AchievementHunter.txt, roosterteeth.txt

# Run the command (for Windows or Linux)

This command reads in that file of YouTube links, sorts them randomly (to help avoid conflicts with others), and then loops through them one by one and runs the tubeup command on them


### Helpful Resource
[Navigating in Powershell](https://www.itprotoday.com/powershell/how-use-powershell-navigate-windows-folder-structure)

## Windows:
- Open Powershell
- Navigate to the folder where the file your downloaded file is located (or copy the file to the folder when powershell opens)

- You can now run the following command in Powershell to run tubeup, replacing [channelname] with the chosen file name:
	

```
Get-Content -Path ./[channelname].txt | Sort-Object {Get-Random} | ForEach-Object {
    tubeup --use-download-archive $_
}
```



## Linux:
Run the following in your shell, replacing [channelname] with the chosen file name:

`shuf [channelname].txt | xargs -I {} tubeup --use-download-archive {}`
