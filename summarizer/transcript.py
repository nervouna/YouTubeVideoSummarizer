import logging
import urllib.parse
from youtube_transcript_api import YouTubeTranscriptApi


def _get_youtube_video_id(video_url: str) -> str:
    """
    Get the video ID from the video URL
    """
    query = urllib.parse.urlparse(video_url).query
    return urllib.parse.parse_qs(query)["v"][0]


def _get_youtube_transcript_from_url(url: str, languages: list[str]) -> dict:
    """
    Get the transcript from the video URL
    """
    video_id = _get_youtube_video_id(url)
    logging.info(f"Getting transcript for video ID {video_id}")
    return YouTubeTranscriptApi.get_transcript(video_id, languages=languages)


def _merge_transcript_text(transcript: dict) -> str:
    """
    Merge the transcript text from the transcript
    """
    return "\n".join([line["text"] for line in transcript])


def get_youtube_transcript_text(url: str, languages: list[str] = ["en"]) -> str:
    """
    Get the transcript text from the video URL
    """
    transcript = _get_youtube_transcript_from_url(url, languages=languages)
    return _merge_transcript_text(transcript)
