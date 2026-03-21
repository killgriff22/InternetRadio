"""
this file is malformed, and full of old code. 
it exiosts to push missing import errors out of the main program.
"""

class StreamOps:# Legacy code for Internet Radio
    def download_sample(stream, seconds):
        stream_url = 'https://www.partyvibe.com:8061/;listen.pls?sid=1'
        r = requests.get(stream_url, stream=True)
        start_time = time.time()
        with open('stream.mp3', 'wb') as f:
            for block in r.iter_content(1024):
                delta = time.time()-start_time
                print(delta)
                if delta >= seconds:
                    break
                f.write(block)


    def generate_frames(seconds, fps):
        image = Image.new("RGB", (853, 480), (0,0,0))
        for j in tqdm.tqdm(range(seconds*fps)):
           image.save(f"generate/{j}.png")

    def generate_video(seconds, fps):
        # choose codec according to format needed
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        video = cv2.VideoWriter('video.mp4', fourcc, fps, (853, 480))
        img = cv2.imread('generate/0' + '.png')
        for j in tqdm.tqdm(range(seconds*fps)):
           video.write(img)
        cv2.destroyAllWindows()
        video.release()

    def convert_stream(inputfile):
        _args = ['-i',inputfile,'-i','video.mp4','-strict','-2','-y','-c:a','vorbis','-c:v','vp8','../stream.webm']
        if platform.system().lower() == "linux":
            os.system(f'./ffmpeg -i {inputfile} -i video.mp4 -strict -2 -y -c:a vorbis -c:v vp8 ../stream.webm')
            #a = subprocess.run(args=_args,executable="./ffmpeg")
        elif platform.system().lower() == "windows":
            os.system(f'./ffmpeg.exe -i {inputfile} -i video.mp4 -strict -2 -y -c:a vorbis -c:v vp8 ../stream.webm')
            #subprocess.run(args=_args, executable="ffmpeg.exe")

class FileOps: # Legacy Interop code, may be repurposed later.