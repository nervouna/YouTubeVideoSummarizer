## TL;DR

This script summarizes YouTube video transcripts and outputs them to the console. It can also translate the summary into other languages.

## Why I came up with this

I don't know when it started, but YouTube videos (especially technical videos) have become increasingly fancy. Almost every video has a 5-minute introduction, a 5-minute conclusion, and various exaggerated transition effects in between. A 1-hour video may only contain 10 minutes of actual information.

For instance, this [lengthy video](https://www.youtube.com/watch?v=w-X_EQ2Xva4) used 1 hour and 14 minutes to explain how to make an API call. The same information can be acquired with a 10-minute read on the [OpenAI docs site](https://platform.openai.com/docs/quickstart/build-your-application).

Time is money, my friend. To save time skipping through the progress bar and watching at an accelerated speed, I came up with a small script. It fetches video content summaries in advance, and then I decide whether it's worth spending time watching.

## How it works

It's quite simple: the script uses the [YouTube Transcript API package](https://github.com/jdepoix/youtube-transcript-api) to fetch the transcripts, merges the time series text into one giant string, and then throws it to the [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create).

If the merged transcript is too long (exceeds the token limit), the script will split it into multiple parts and summarize them separately. Then it will merge the summaries into one and summarize again. There's a recursion limit (which defaults to 3), so the script won't run forever.

And if, for some reason, the video doesn't have any transcripts, you can use the `--transcribe` flag (or `-t` for short) to download the video using the [PyTube package](https://github.com/pytube/pytube/issues/1684), transcribe the video file with [the Whisper model](https://github.com/openai/whisper), and summarize it.

## Usage

![Screenshot](https://github.com/nervouna/YouTubeVideoSummarizer/blob/main/screenshot.png)

Rename the `example.env` to `.env` and fill in the variables.

```bash
# Requirements:
pip install -r requirements.txt

# Basic usage:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4

# Using whisper:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 -t

# Output only the summary (in case you need to use it in a pipeline):
# For example, you can pipe the output to a text-to-speech program:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 -q | say

# With Azure OpenAI API:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 --azure

# Translate the summary to a certain language:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 --translate-to Japanese
```

> **Note**: Downloading and transcribing the video file is a time-consuming process. It may take a few minutes to complete. Use the `-t` parameter only when the default method fails.

## Todo

- [x] Get video transcripts
- [x] Summarize transcripts
- [x] Split long transcripts if they exceed the token limit
- [x] Download video, transcribe the video file, and summarize it

## License

[WTFPL](http://www.wtfpl.net/)