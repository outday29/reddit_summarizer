from pathlib import Path

import openai
import yaml
from settings import settings

from scraper.models import Summary

openai.api_key = settings.openai_key
prompt_path = Path("./prompt.txt")
model_name = "gpt-3.5-turbo"


def summarize_thread(thread_path: Path, output_path: Path):
    def write_summary(summary_obj: Summary):
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump((summary_obj.dict()), f)

    text = thread_path.read_text(encoding="utf-8")
    thread_dict = yaml.safe_load(text)
    prompt_prefix = prompt_path.read_text(encoding="utf-8")
    prompt = prompt_prefix + "\n\n" + text
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    gpt_response = response["choices"][0]["message"]["content"]
    summary_obj = Summary(
        title=thread_dict["title"],
        link=thread_dict["link"],
        user=thread_dict["op"],
        description=gpt_response,
    )
    write_summary(summary_obj)
