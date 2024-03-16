# TubeUp Installation Tutorial:

### Run PowerShell as Admin
> Win+X => Choose " PowerShell (Administrator) "

### Install Chocolatey
Following these 5 steps: https://chocolatey.org/install
	- Chocolatey is a package manager which can be used to install other software

### Install Python
Type this line (source: https://docs.python-guide.org/starting/install3/win/#install3-windows)
`choco install python`
	- Note, you will likely need to restart after this

### Check and upgrade pip:
Pip is python's own package manager, which is used to install python libraries
`py -m pip install -U pip`


### Install setuptools
Otherwise it may throw an error that pkg_resources is missing
`pip install setuptools`

### Install TubeUp
`pip install tubeup`

It will ask you whether you want to install a package for every package it downloads. Press "A" key to say yes to all


### Set up ffmpeg:
 * download an archive with ffmpeg, ffplay and ffprobe from here: 

 * Unarchive the folder and copy all three .exe from bin folder
 * Paste the three .exe files in C:\Python312\Scripts


## Now you should have choco, Python, pip, setuptools, tubeup(with ia and yt-dlp), ffmpeg ready
