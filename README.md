# Gearblocks Music Player
the best place to find releases of this mod is on the steam workshop.<br>
This is a scriptmod for the game [GearBlocks](https://store.steampowered.com/app/1305080/GearBlocks/)<br>
Included is a python script to convert any audio or video container (mp3, mp4, flac, webm) into a format friendly to the scriptmod, along with the metadata to run the scriptmod with it's bells and whistles.
# !! IMPORTANT READ ME !!
If your ffmpeg binaries do not work (files fail to convert, many errors appear in the console)<br>
go source a new ffmpeg.exe from [The official mirror list](https://ffmpeg.org/download.html)<br>
Or [directly from github](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)<br>
If you're on linux and experiencing difficulty with ffmpeg, you may need to give the binary executable permission.
# Converting files!
* Make sure you have a recent version of Python 3<br>
[Windows](https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe)
* Run the setup script for your os<br>
Windows: setup.bat<br>
Linux: setup.sh
* Delete everything in the musicConvert and music folders
* Add your music into the musicConvert folder
## The recommended way:
* Run main.py and wait for your files to convert.<br>
Files with qoutes in their names may not work. try to get rid of all  `'` and `"` before converting.
* if the script didnt fatally error, you should be able to start playing music in GearBlocks! 
## The "I've already converted my files and I don't want to again" way
### tldr, the haxor way
* Instead of blindly running main.py, crack it open and use `#` to comment and un comment the FFMpegOps line to enable and disable converting your files.
* Similarly, you can comment out the last few lines to disable the generation of the playlist.lua
<br>
<br>
<br>
<br>
# Copyright
No files included are of copyrighted works.<br>
All files included are products of my work and help of the internet.<br>
NO AI WAS USED IN THE MAKING OF THIS