"""
Entrypoint file. this is the default file to be used for file conversion and auto generation.
see README.md for documentation.
"""
#begin the import chain
from classes import *
# generate frames to be used in video geenration.
# this is largely redundant unless you lose the "0.png" file from the generate folder.
#StreamOps.generate_frames(1,1) 
# sanity check.
print("Frames Generated")
# generate a 10 minute long video at 24 fps. change the minutes variable to change the length of the video used.
#minutes = 10
#StreamOps.generate_video(minutes*60,24)
print("Video Created")

#convert everything to a sane format before converting into webms
for file in os.listdir("../musicConvert/"):
    if not "_PC.mp3" in file:
        FFmpegOps.convert2mp3(file)
        os.remove(file)
print("Pre Processing complete!")

#convert everything in the musicConvert folder to the gearblocks freiendly webm
for file in os.listdir("../musicConvert/"):
    name = file[:-4]
    if platform.system() == "Linux":
        FFmpegOps.convert_files([f"\"../musicConvert/{file}\"", "video.mp4"],f"\"../music/{name}.webm\"")
    else:
        FFmpegOps.convert_files([f"\"..\\musicConvert/{file}\"", "video.mp4"],f"\"..\\music\\{name}.webm\"")
PlaylistOps.GeneratePlaylist()
exit()
