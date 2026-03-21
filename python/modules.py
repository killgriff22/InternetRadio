"""
this file contains the imports for my modules, and defines some specifics that were used for the Interop.
Largely useless, though this is the deepest import, and the most important.
"""


import time, datetime,tqdm
import os
import platform
from  PIL import Image
import cv2
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

os.chdir(os.path.dirname(__file__))
LogPath = "/home/skye/.config/unity3d/SmashHammer Games/GearBlocks/Player.log"
InteropPath = "/home/skye/.config/unity3d/SmashHammer Games/GearBlocks/ScriptMods/InternetRadio/Interop.lua"