import os
import json
import tempfile
from bson import ObjectId
from moviepy.editor import VideoFileClip


def convert_to_mp3(message, fs_videos, fs_mp3s, channel):
    """
    message: raw RabbitMQ message (JSON bytes)
    fs_videos: GridFS for videos
    fs_mp3s: GridFS for mp3 storage
    """

    try:
        message = json.loads(message)
    except Exception as e:
        print("JSON decode error:", e)
        return "bad json"

    video_fid = message.get("video_fid")
    if not video_fid:
        return "missing video_fid"

    try:
        video_file = fs_videos.get(ObjectId(video_fid))
    except Exception as e:
        print("GridFS video fetch error:", e)
        return "video not found"

    # -------------------------------
    # Create temp input file
    # -------------------------------
    input_tmp = tempfile.NamedTemporaryFile(delete=False)
    input_tmp.write(video_file.read())
    input_tmp.close()

    # -------------------------------
    # Convert video → mp3
    # -------------------------------
    output_tmp = tempfile.gettempdir() + f"/{video_fid}.mp3"

    try:
        clip = VideoFileClip(input_tmp.name)
        clip.audio.write_audiofile(output_tmp, logger=None)
        clip.close()
    except Exception as e:
        os.remove(input_tmp.name)
        print("Conversion error:", e)
        return "ffmpeg error"

    os.remove(input_tmp.name)

    # -------------------------------
    # Save mp3 to MongoDB GridFS
    # -------------------------------
    try:
        with open(output_tmp, "rb") as f:
            file_id = fs_mp3s.put(f.read())
    except Exception as e:
        print("GridFS mp3 save error:", e)
        return "gridfs write error"
    finally:
        os.remove(output_tmp)

    # Store MP3 file_id back into message
    message["mp3_fid"] = str(file_id)

    # -------------------------------
    # Publish new message to MP3_QUEUE
    # -------------------------------
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE", "mp3"),
            body=json.dumps(message),
            properties=None,
        )
    except Exception as e:
        print("RabbitMQ publish error:", e)
        fs_mp3s.delete(file_id)
        return "publish error"

    return None  # success
