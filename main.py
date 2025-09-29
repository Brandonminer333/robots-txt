import os

import requests
from google import genai
from dotenv import load_dotenv
from google.genai import types


def input_checker(url):
    if "robots.txt" in url:
        return url
    else:
        return url+"/robots.txt"


def parse_robots(url):
    text = requests.get(url).text
    links = get_links(text)
    return text, links


def get_links(text):
    list_text = text.split()
    links = [link for link in list_text if "http" in list_text]
    if links == []:
        return None
    else:
        return links


load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
system_instruction = """
From the given string, identify what is and is not allowed to be scraped on a websie according to their robots.txt.

What you need to provide is just a string of what is and isn't allowed.
"""

website = input("Submit a website: ")
website = input_checker(website)

text, links = parse_robots(website)

client = genai.Client(api_key=gemini_key)
model_name = "gemini-2.5-flash"


if links is not None:
    for link in links:
        parse_robots(link)
else:
    response = client.models.generate_content(
        model=model_name,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction),
        contents=text
    )

print(response.text)
