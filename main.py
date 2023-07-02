from summarizer.transcript import get_youtube_transcript_text
from summarizer.summarizer import summarize
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("url", type=str, help="URL of the YouTube video.")
    parser.add_argument("--translate-to", type=str,
                        help="Language to translate the summary to.")
    parser.add_argument("--azure", action="store_true",
                        help="Use Azure OpenAI API.")
    parser.add_argument("--quiet", action="store_true",
                        help="Only prints the summary.")
    args = parser.parse_args()

    summary = summarize(
        get_youtube_transcript_text(args.url),
        translate_to=args.translate_to,
        azure=args.azure,
        quiet=args.quiet
    )
    print(summary)
