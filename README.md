# Youtube Video Summarizer

## TL;DR

This script summarizes YouTube video transcripts and outputs them to the console. It can also translate the transcripts into other languages. 

## Description

I don't know when it started, but YouTube videos (especially technical videos) have become increasingly fancy. Almost every video has a 5-minute introduction, a 5-minute conclusion, and various exaggerated transition effects in between. A 30-minute video may only contain 10 minutes of actual information. 

To save time skipping through the progress bar and watching in accelerated speed, I came up with a small script. It fetches video content summaries in advance, and then I decide whether it's worth spending time watching.

Note that the script currently only works with videos with transcripts/captions. However, I plan to add audio transcription as a fallback.

## Usage

Rename the `example.env` to `.env` and fill in the varialbes.

```bash
# Requirements:
pip install -r requirements.txt

# Basic usage:
python main.py https://www.youtube.com/watch?v=WtMrp2hp94E

# Output only the summary (in case you need to use it in a pipeline):
python main.py https://www.youtube.com/watch?v=WtMrp2hp94E --quiet

# With Azure OpenAI API:
python main.py https://www.youtube.com/watch?v=WtMrp2hp94E --azure

# Or if you are not comfortable with the original language:
python main.py https://www.youtube.com/watch?v=WtMrp2hp94E --translate-to Japanese
```

Output:

```
Starting summarization round 1...

100%|████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:04<00:00,  4.56s/it]
Round 1 complete, used 3147 tokens.

The video discusses how to automate the process of extracting audio from a YouTube video, transcribing the audio, and generating a summary using ChatGPT. The process involves using libraries such as librosa, YouTube DL, and sound file, as well as the OpenAI API. The code provided in the video demonstrates how to download the YouTube video, chunk the audio into smaller segments, transcribe the audio using the whisper model, and summarize the transcriptions using ChatGPT. The video also includes a wrapper function that combines all the steps into a single process. The code and instructions are provided in the video for reference.
```

## Todo

- [x] Get video transcripts
- [x] Summarize transcripts
- [x] Split long transcripts if exceeds token limit
- [ ] Download video and convert into audio file
- [ ] Transcribe the audio file and summarize it

## License

[WTFPL](http://www.wtfpl.net/)
