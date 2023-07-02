# Youtube Video Summarizer

## TL;DR

This script summarizes YouTube video transcripts and outputs them to the console. It can also translate the summary into other languages. 

## Description

I don't know when it started, but YouTube videos (especially technical videos) have become increasingly fancy. Almost every video has a 5-minute introduction, a 5-minute conclusion, and various exaggerated transition effects in between. A 1-hour video may only contain 10 minutes of actual information. 

> For instance: This [lengthy video](https://www.youtube.com/watch?v=w-X_EQ2Xva4) used 1 hour and 14 minutes to explain how to make an API call. The same information can be aquired with a 10-minutes read on the [OpenAI docs site](https://platform.openai.com/docs/quickstart/build-your-application).

Time is money, my friend. To save time skipping through the progress bar and watching in accelerated speed, I came up with a small script. It fetches video content summaries in advance, and then I decide whether it's worth spending time watching.

Note that the script currently only works with videos with transcripts/captions. However, I plan to add audio transcription as a fallback in the future.

## Usage

Rename the `example.env` to `.env` and fill in the varialbes.

```bash
# Requirements:
pip install -r requirements.txt

# Basic usage:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4

# Output only the summary (in case you need to use it in a pipeline):
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 --quiet

# With Azure OpenAI API (remember to set the variables in .env):
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 --azure

# Or if you are not comfortable with the original language:
python main.py https://www.youtube.com/watch?v=w-X_EQ2Xva4 --translate-to Japanese
```

## Todo

- [x] Get video transcripts
- [x] Summarize transcripts
- [x] Split long transcripts if exceeds token limit
- [ ] Download video and convert into audio file
- [ ] Transcribe the audio file and summarize it

## License

[WTFPL](http://www.wtfpl.net/)
