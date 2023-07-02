from argparse import ArgumentParser
from summarizer.summarizer import summarize
from summarizer.transcriber import download_and_transcribe
from summarizer.transcript import get_youtube_transcript_text
import logging


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("url", type=str, help="URL of the YouTube video.")
    parser.add_argument("--translate-to", type=str,
                        help="Language to translate the summary to.")
    parser.add_argument("--azure", action="store_true",
                        help="Use Azure OpenAI API.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress output except for the summary.")
    parser.add_argument("-t", "--transcribe", action="store_true",
                        help="Download the video and use whisper model to transcribe it.")
    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.transcribe:
        text = download_and_transcribe(args.url)
    else:
        text = get_youtube_transcript_text(args.url)

    summary = summarize(
        text,
        translate_to=args.translate_to,
        azure=args.azure,
        quiet=args.quiet
    )
    print(summary)
