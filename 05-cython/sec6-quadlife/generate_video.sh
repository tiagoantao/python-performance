rm frame-0*
rm video.mp4
python generate_video.py
ffmpeg -framerate 14 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p video_small.mp4
ffmpeg -i video_small.mp4 -vf scale=-2:1080 -sws_flags area video.mp4
rm video_small.mp4
