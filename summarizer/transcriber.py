from summarizer.suppress_warning import *

import os
import whisper
import logging
from pytube import YouTube
from pytube.cli import on_progress
from http.client import IncompleteRead

_DATA_ROOT = "data"
_MODEL_DIR = "models"
_MODEL_NAME = "base"
_VIDEO_DIR = "videos"


def _create_folders():
    """
    Create the folders if they don't exist
    """
    logging.info("Creating folders...")
    if not os.path.exists(_DATA_ROOT):
        os.makedirs(_DATA_ROOT)

    model_path = os.path.join(_DATA_ROOT, _MODEL_DIR)
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    video_path = os.path.join(_DATA_ROOT, _VIDEO_DIR)
    if not os.path.exists(video_path):
        os.makedirs(video_path)


def _fetch_video_stream(video_url):
    if logging.INFO >= logging.root.level:
        yt = YouTube(video_url, on_progress_callback=on_progress)
    else:
        yt = YouTube(video_url)
    logging.info("Fetching video info...")
    video = yt.streams.filter(progressive=True, file_extension="mp4").order_by(
        "resolution").first()
    return video


def _download_video(video_url: str) -> str:
    """
    Download the video from the video URL
    """
    _create_folders()
    video_path = os.path.join(_DATA_ROOT, _VIDEO_DIR)
    video = _fetch_video_stream(video_url)
    try:
        logging.info("Downloading video...")
        video.download(video_path)
    except IncompleteRead:
        logging.warning("Incomplete read, ignored.")
        pass
    return video.default_filename


def _delete_downloaded_videos():
    """
    Delete the downloaded videos
    """
    logging.info("Deleting downloaded videos...")
    video_path = os.path.join(_DATA_ROOT, _VIDEO_DIR)
    for file in os.listdir(video_path):
        os.remove(os.path.join(video_path, file))


def _load_model() -> whisper.Whisper:
    """
    Load the model from the file system
    """
    logging.info(
        "Loading model. If this is the first run, it's gonna take a while...")
    model_path = os.path.join(_DATA_ROOT, _MODEL_DIR)
    return whisper.load_model(_MODEL_NAME, download_root=model_path)


def _transcribe(video_file_name: str) -> str:
    """
    Transcribe the video file
    """
    model = _load_model()
    logging.info("Transcribing video...")
    video_path = os.path.join(_DATA_ROOT, _VIDEO_DIR, video_file_name)
    result = model.transcribe(video_path)
    return result["text"]


def download_and_transcribe(video_url: str, verbose: bool = False, clean_up: bool = True) -> str:
    """
    Download the video, load the base whisper model,
    transcribe it into text, and delete the downloaded video
    """
    video_file_name = _download_video(video_url)
    text = _transcribe(video_file_name)
    if clean_up:
        _delete_downloaded_videos()
    return text
