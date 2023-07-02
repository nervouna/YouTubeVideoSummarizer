import os
import openai
import tiktoken
import logging

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

_OPENAI_INITIALIZED = False
_GPT_MODEL = "gpt-3.5-turbo"
_DEPLOYMENT_ID = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
_MAX_TOKENS = 3000
_MAX_SUMMARIZE_RECURSION = 3


def _init_azure_openai():
    """
    Initialize the Azure OpenAI configuration
    """
    openai.api_type = "azure"
    openai.api_key = os.getenv("AZURE_OPENAI_KEY")
    openai.api_base = os.getenv("AZURE_OPENAI_HOST")
    openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not openai.api_type or not openai.api_key or not openai.api_base or not openai.api_version or not _DEPLOYMENT_ID:
        raise Exception("Azure OpenAI API not configured correctly.")

    global _OPENAI_INITIALIZED
    _OPENAI_INITIALIZED = True


def _init_openai():
    """
    Initialize the OpenAI configuration
    """
    openai.api_key = os.getenv("OPENAI_KEY")
    openai.api_base = os.getenv("OPENAI_HOST")

    if not openai.api_key:
        raise Exception("OpenAI API not configured correctly.")

    global _OPENAI_INITIALIZED
    _OPENAI_INITIALIZED = True


def _count_tokens(text: str, model: str) -> int:
    """
    Count the number of tokens in the given text using the specified model
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def _split_long_text(text: str, max_tokens: int) -> list[str]:
    """
    Split the text into multiple strings with a maximum number of tokens
    """
    tokens = _count_tokens(text, model=_GPT_MODEL)
    if tokens < max_tokens:
        return [text]

    # Split the text into multiple strings
    chunks = []
    lines = text.split("\n")
    chunk = ""

    for line in lines:
        if _count_tokens(chunk + line, model=_GPT_MODEL) < max_tokens:
            chunk += line + "\n"
        else:
            chunks.append(chunk)
            chunk = line + "\n"

    return chunks


def _assemble_prompt(chunk: str, translate_to: str) -> dict:
    """
    Assemble the prompt for the GPT-3 model
    """
    prompt = "Provide a concise summary of the video transcript " + \
        "while maintaining accuracy and encouraging creativity in the response. "

    if translate_to:
        prompt += f"\n\nThe summary should written in {translate_to}."

    prompt += "\n\nTranscription:\n\n{}\n\nSummary:\n\n"

    return {"role": "user", "content": prompt.format(chunk)}


def _azure_completion(deployment_id, message):
    if not _OPENAI_INITIALIZED:
        _init_azure_openai()

    response = openai.ChatCompletion.create(
        deployment_id=deployment_id,
        messages=[message],
        temperature=0,
    )

    return response


def _openai_completion(model, message):
    if not _OPENAI_INITIALIZED:
        _init_openai()

    response = openai.ChatCompletion.create(
        model=model,
        messages=[message],
        temperature=0,
    )
    return response


def _get_completion(translate_to, azure, deployment_id, chunk):
    message = _assemble_prompt(chunk, translate_to=translate_to)
    if azure:
        response = _azure_completion(deployment_id, message)
    else:
        response = _openai_completion(_GPT_MODEL, message)
    return response


def summarize(text: str, translate_to: str, azure: bool,
              deployment_id: str = _DEPLOYMENT_ID,
              recursion: int = _MAX_SUMMARIZE_RECURSION,
              quiet: bool = False) -> str:
    """
    Summarize the text using the GPT-3 model
    """
    # Split the text into multiple strings
    chunks = _split_long_text(text, max_tokens=_MAX_TOKENS)

    summaries = []
    summarize_round = _MAX_SUMMARIZE_RECURSION - recursion + 1

    tokens = 0

    if quiet:
        for chunk in chunks:
            response = _get_completion(
                translate_to, azure, deployment_id, chunk)
            summaries.append(response.choices[0].message.content)
    else:
        logging.info(f"Starting summarization round {summarize_round}...")
        for chunk in tqdm(chunks):
            response = _get_completion(
                translate_to, azure, deployment_id, chunk)
            summaries.append(response.choices[0].message.content)
            tokens += response.usage.total_tokens
        logging.info(
            f"Round {summarize_round} complete, used {tokens} tokens.")

    recursion -= 1
    summary_str = "\n".join(summaries)

    if len(summaries) > 1 and recursion > 0:
        return summarize(summary_str, azure=azure,
                         translate_to=translate_to, recursion=recursion, quiet=quiet)
    else:
        return summary_str
