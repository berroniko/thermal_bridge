import json
import os
from datetime import datetime
from pathlib import Path

import ollama
from openai import OpenAI
from prompt_toolkit import prompt
from pydantic import BaseModel

from src import SRC_ROOT

working_locally = False

if working_locally:
    with open(SRC_ROOT.parent.parent / Path("credentials.json")) as f:
        credentials = json.load(f)

    os.environ['echo'] = credentials["openai_api_testing"]


def is_nan(value) -> bool:
    if isinstance(value, float):
        if value != value:
            return True
        else:
            return False
    if not value:
        return True
    else:
        return False


def input_with_default(message: str, default: str) -> str:
    return prompt(message, default=default)


def parse_date(date_str: str) -> datetime:
    for fmt in ('%d.%m.%Y', '%d,%m,%Y', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # olla_ = parse_date_ollama(date_string=date_str)
    # olla_ = parse_date_chatgpt(date_string=date_str)
    olla_ = parse_structured_date_chatpgpt(date_string=date_str)

    if olla_:
        olla_date = olla_.get('date')
        try:
            return datetime.strptime(olla_date, '%d.%m.%Y')
        except ValueError:
            pass

    # user_input = input_with_default(message="please correct this to the format dd.mm.yyyy:",
    #                                 default=date_str)
    user_input = input(f"please enter this date '{date_str}' in format dd.mm.yyyy:")
    return parse_date(user_input)


def parse_date_ollama(date_string: str) -> dict:
    """format date and correct errors using ollama.

    Args
        date_string: str

    Returns
        { "date": "dd.mm.yyyy" }
    """
    client = ollama.Client()
    model = "llama3.2"
    # model = "deepseek-r1:1.5b"

    prompt = f"""
    You are a date parser. I will give you a string representing a date between 2015 and today, 
    which may have inconsistent formatting, typos or errors like 
    - extra zeros 
    - missing zeros
    - inverted position of day and month.

    Normalize the date in the format "dd.mm.yyyy" and return it as JSON like this: {{ "date": "dd.mm.yyyy" }}.

    Input: "{date_string}"
    """

    response = client.generate(model=model, prompt=prompt, format="json", stream=False)

    return json.loads(response.response)


def parse_date_chatgpt(date_string: str) -> dict | None:
    client = OpenAI()
    # OPENAI_API_KEY
    prompt = f"""
    You are a date parser. I will give you a string representing a date between 2015 and today, 
    which may have inconsistent formatting or minor errors like extra zeros.

    Return the date in the format "dd.mm.yyyy" as JSON like this: {{ "date": "dd.mm.yyyy" }}.

    {date_string}
    """

    # Call the model
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-4o" or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You format messy date strings to dd.mm.yyyy format in JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    # Extract and print the result
    result = response.choices[0].message.content
    print(f"date: {date_string}, AI: {result}")
    if result and len(result) == 10:
        return json.loads(result)
    # elif   # 2nd attempt
    else:
        return None


def parse_structured_date_chatpgpt(date_string: str) -> dict | None:
    client = OpenAI()
    # OPENAI_API_KEY
    prompt = f"""
    You are a date parser. I will give you a string representing a date between 2012 and today, 
    which may have inconsistent formatting or minor errors like extra zeros.

    Return the date in the format "dd.mm.yyyy" as JSON like this: {{ "date": "dd.mm.yyyy" }}.

    {date_string}
    """

    class DateClass(BaseModel):
        date: str

    # Call the model
    response = client.responses.parse(
        model="gpt-4o-2024-11-20",  # or "gpt-4o" or "gpt-3.5-turbo"
        input=[
            {"role": "system", "content": "You format messy date strings to dd.mm.yyyy format in JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        text_format=DateClass,
    )
    return response.output_parsed.model_dump()


if __name__ == '__main__':
    # result = input_with_default("please correct: ", default="hällo")
    result = parse_date("09/24.2018")
    print(result)
