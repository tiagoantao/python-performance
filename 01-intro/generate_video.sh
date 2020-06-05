rm frame-0*
rm video.mp4
python generate_video.py
ffmpeg -framerate 14 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p video.mp4
