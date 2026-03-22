from functions import *
"""
this file contains the bulk of my implementations.
included alongside these scripts there should be FFMPEG binaries for both linux and windows.
if you find that the included binaries do not work, extra binaries can be found at: 
https://ffmpeg.org/download.html
Windows: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
Linux: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz
"""
class FFmpegOps: # logic for converting the files using a pre-generated mp4 as the video source
    def convert_files(input, outputname):
        ichain = " -i "+(' -i '.join(input))
        cmd = ichain + " -c:v vp8 -c:a vorbis -strict -2 -n " + outputname
        if platform.system() == "Linux":
            cmd = "./ffmpeg.x86_64 " + cmd
        else:
            cmd = "ffmpeg.exe " + cmd
        os.system(cmd)
    def convert2ogg(file):
        ext = file[:-3]
        if not ext[-1] == ".":
            ext = file[:-5]
        else:
            ext = file[:-4]
        badname = any(op in ext for op in ['\'','"','`', " "])
        while badname:
            print(ext)
            [ext := ext.replace(op,"") for op in ['\'','"','`', " ","[","]"]]
            badname = any(op in ext for op in ['\'','"','`', " ","[","]"])
        if platform.system() == "Linux":
            cmd = f" -i '../musicConvert/{file}' -strict -2 '../musicConvert/{ext}_PC.mp3'" # PC meansd Post Convert
            cmd = "./ffmpeg.x86_64 " + cmd
        else:
            cmd = f" -i '..\\musicConvert\\{file}' -strict -2 '..\\musicConvert\\{ext}_PC.mp3'" # PC meansd Post Convert
            cmd = "ffmpeg.exe " + cmd
        os.system(cmd)

class StreamOps:# code for generating video

    def generate_frames(seconds, fps):
        image = Image.new("RGB", (853, 480), (0,0,0))
        for j in tqdm.tqdm(range(seconds*fps)):
           image.save(f"generate/{j}.png")

    def generate_video(seconds, fps):
        # choose codec according to format needed
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        video = cv2.VideoWriter('video.mp4', fourcc, fps, (853, 480))
        img = cv2.imread('generate/0.png')
        for j in tqdm.tqdm(range(seconds*fps)):
           video.write(img)
        cv2.destroyAllWindows()
        video.release()


class PlaylistOps: # generate the library files nesscary to pickup tracks
    def GeneratePlaylist():
        GeneratedFiles = os.listdir("../music")
        Playlist = """return {\n    Location = ScriptPath.."/music",\n    files={\n"""
        for i in range(len(GeneratedFiles)):
            Playlist += f"        [{i+1}] = [[{GeneratedFiles[i]}]],\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    titles = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            track = name
            if name in str(os.listdir("../musicConvert")):
                track = ID3(f"../musicConvert/{name}.mp3")
                if 'TIT2' in track.keys():
                    track = track['TIT2'].text[0]
                else:
                    track = name
            Playlist += f"        [{i+1}] = [[{track}]],\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    lengths = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            length = 10*60
            if name in str(os.listdir("../musicConvert")):
                length = int(MP3(f"../musicConvert/{name}.mp3").info.length//1)
            Playlist += f"        [{i+1}] = {length},\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    artists = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            artist = "UNKOWN"
            if name in str(os.listdir("../musicConvert")):
                artist = ID3(f"../musicConvert/{name}.mp3")
                if 'TPE1' in artist.keys():
                    artist = artist['TPE1'].text[0]
                else:
                    artist = "UNKNOWN"
            Playlist += f"        [{i+1}] = [[{artist}]],\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    albums = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            album = "UNKOWN"
            if name in str(os.listdir("../musicConvert")):
                album = ID3(f"../musicConvert/{name}.mp3")
                if 'TALB' in list(album.keys()):
                    album = album["TALB"].text[0]
                else:
                    album = "UNKOWN"
            Playlist += f"        [{i+1}] = [[{album}]],\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    }\n}"
        print(Playlist)
        return Playlist