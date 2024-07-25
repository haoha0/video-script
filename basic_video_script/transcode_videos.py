import os
# 视频处理
'''
六种分辨率级别:
144p: 256x144
240p: 426x240
360p: 640x360
480p: 854x480
720p: 1280x720
1080p: 1920x1080
'''

FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"    # 需要适应修改 TODO
MP4BOX_PATH = "/usr/local/bin/Mp4Box"       # 需要适应修改 TODO

input_dir = "videos"
output_dir = "videos_output"
output_mpd_dir = "mpds_output"

resolutions = {
    "144p": "256x144",
    "240p": "426x240",
    "360p": "640x360",
    "480p": "854x480",
    "720p": "1280x720",
    "1080p": "1920x1080"
}

# transcode video
def transcode_video(input_file, output_file, resolution):
    cmd_video = f"{FFMPEG_PATH} -i {input_file} -vf scale={resolution} -c:v libx264 -crf 23 -preset veryfast -an {output_file}"
    os.system(cmd_video)

# transcode audio
def transcode_audio(input_file, output_file):
    cmd_audio = f"{FFMPEG_PATH} -i {input_file} -c:a aac -b:a 128k -vn {output_file}"
    os.system(cmd_audio)

# mp4box
def process_mp4box(input_audio, input_videos, frag_size, output_mpd):
     # MP4Box -dash 5000 -rap -frag-rap -profile dashavc264:onDemand -frag 5000 input_audio_128k.mp4 input_video_160x90_250k.mp4 input_video_320x180_500k.mp4 input_video_640x360_750k.mp4 input_video_640x360_1000k.mp4 input_video_1280x720_1500k.mp4 -out main.mpd
    cmd_mp4box = (
        f"{MP4BOX_PATH} -dash {frag_size} -rap -frag-rap -profile dashavc264:onDemand -frag {frag_size} "
        f"{input_audio} "
        f"{input_videos[0]} "
        f"{input_videos[1]} "
        f"{input_videos[2]} "
        f"{input_videos[3]} "
        f"{input_videos[4]} "
        f"{input_videos[5]} "
        f"-out {output_mpd}"
    )
    os.system(cmd_mp4box)

# 对每种分辨率进行转码
for sub_dir in os.listdir(input_dir):
    sub_dir_path = os.path.join(input_dir, sub_dir)
    if os.path.isdir(sub_dir_path):
        print(f"Processing directory: {sub_dir_path}")
        for file in os.listdir(sub_dir_path):
            file_path = os.path.join(sub_dir_path, file)
            if file.endswith(".mp4"):
                name = os.path.splitext(file)[0]
                print(f"Transcode video: {name}.")
                # 视频转码
                output_videos = []
                for label, res in resolutions.items():
                        print(f"Processing video transcoding for video {name} with resolution {res}.")
                        input_video = os.path.join(sub_dir_path, file)
                        output_video = os.path.join(output_dir, f"{name}_{label}.mp4")
                        transcode_video(input_video, output_video, res)
                        output_videos.append(output_video)

                # 音频转码
                print(f"Processing audio transcoding for video {name}.")
                input_video = os.path.join(sub_dir_path, file)
                output_audio = os.path.join(output_dir, f"{name}_audio.m4a")
                transcode_audio(input_video, output_audio)

                # 用 mp4box 得到 MPEG-Dash 需要的音视频和 .mpd 文件
                frag_size = 5000 # 片段大小设置为5s，可以修改 TODO
                output_mpd = os.path.join(output_mpd_dir, f"{name}.mpd")
                print(f"Processing MP4Box to generate mpd file for video {name} with frag size {frag_size}.")
                process_mp4box(output_audio, output_videos, frag_size, output_mpd)

                # 删除videos_output中的文件
                for video in output_videos:
                    os.remove(video)
                os.remove(output_audio)


                print("--------------------------------------------------")
                print(f"Transcode finished for video {name}.")
                print("--------------------------------------------------")
        
print("Transcode finished.")

# 文件传输测试
# scp -r mpds_output/* root@47.94.151.36:/usr/local/nginx/html/

