import os.path
import sys

DIR_RAW_VIDEOS = "raw_videos"
DIR_CLIPS = "../video_clips"


def path_relative(path):
    return os.path.join(
        os.path.dirname(sys.modules["__main__"].__file__), path
    )
