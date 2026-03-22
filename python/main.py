"""
Entrypoint file. this is the default file to be used for file conversion and auto generation.
see README.md for documentation.
"""
#some options for debugging and to speed up the process of conversion/playlist generation.
PRE_CONVERT = True
CONVERT = True
GENERATE_PLAYLIST = True
GENERATE_FRAME = False
GENERATE_VIDEO = False



#begin the import chain
from classes import *

# if the directories we need dont exist, make them.
exit_ = False
if not os.path.exists("../musicConvert/"):
    os.mkdir("../musicConvert")
    exit_ = True
if not os.path.exists("../music/"):
    os.mkdir("../music")
    exit_ = True
#if we had to make new directories, there's nothing to convert. exit.
if exit_:
    exit()



# generate frames to be used in video generation.
# this is largely redundant unless you lose the "0.png" file from the generate folder.
if GENERATE_FRAME:
    StreamOps.generate_frames(1,1) 
    # sanity check.
    print("Frames Generated")
# generate a 10 minute long video at 24 fps. change the minutes variable to change the length of the video used.
if GENERATE_VIDEO:
    minutes = 10
    StreamOps.generate_video(minutes*60,24)
    print("Video Created")



if PRE_CONVERT:
    #convert everything to a sane format before converting into webms
    for file in os.listdir("../musicConvert/"):
        if not "_PC.mp3" in file:
            FFmpegOps.convert2mp3(file)
            os.remove(f"../musicConvert/{file}")
    print("Pre Processing complete!")
if CONVERT:
    #convert everything in the musicConvert folder to the gearblocks freiendly webm
    for file in os.listdir("../musicConvert/"):
        name = file[:-4]
        if platform.system() == "Linux":
            FFmpegOps.convert_files([f"\"../musicConvert/{file}\"", "video.mp4"],f"\"../music/{name}.webm\"")
        else:
            FFmpegOps.convert_files([f"\"..\\musicConvert/{file}\"", "video.mp4"],f"\"..\\music\\{name}.webm\"")
    print("Conversion Finished!")
if GENERATE_PLAYLIST:
    PlaylistOps.GeneratePlaylist()
exit()
