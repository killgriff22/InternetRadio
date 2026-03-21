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
        cmd = ichain + " -c:v vp8 -c:a vorbis -strict -2 -y " + outputname
        if platform.system() == "Linux":
            cmd = "./ffmpeg.x86_64 " + cmd
        else:
            cmd = "./ffmpeg.exe " + cmd
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
            if name in str(GeneratedFiles):
                track = ID3(f"../musicConvert/{name}.mp3")['TIT2'].text[0]
            Playlist += f"        [{i+1}] = [[{track}]],\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    lengths = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            length = 10*60
            if name in str(GeneratedFiles):
                length = int(MP3(f"../musicConvert/{name}.mp3").info.length//1)
            Playlist += f"        [{i+1}] = {length},\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    artists = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            artist = "UNKOWN"
            if name in str(GeneratedFiles):
                artist = ID3(f"../musicConvert/{name}.mp3")['TPE1'].text[0]

            Playlist += f"        [{i+1}] = [[{artist}]],\n"
        Playlist = Playlist[:-2]# remove leading comma
        Playlist += "\n    },\n    albums = {\n"
        for i in range(len(GeneratedFiles)):
            name = GeneratedFiles[i][:-5]
            album = "UNKOWN"
            if name in str(GeneratedFiles):
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


    def writeValues(DictValues):
        w = open(InteropPath,"w")
        w.seek(0)
        w.write(f"""-- Genertated using python
    return {"{"}
        {("".join([f"{k} = '{DictValues[k]}',\n" for k in DictValues.keys()]))[:-2]}
    {"}"}
    """)
        w.close()
        del w

    def read_for(search, back=100):
        t = datetime.datetime.now()
        r = open(LogPath,"r")
        lines = r.readlines()
        lines = [line.strip().split("Lua:")[1] if "Lua:" in line else None for line in lines[-back:]]
        while None in lines:
            lines.remove(None)
        for line in lines:
            if search.lower() in line.lower():
                bulk = line.split(":")[1:]
                h,m,s = bulk[-3:]
                if all(b for b in [
                    str(t.hour) in h,
                    str(t.minute) in m,
                    str(t.second) in s  ]):
                    data = [bulk[:-3],bulk[-3:]]
                    return [True, data, line]
        r.close()
        del r
        return [False, None, None]