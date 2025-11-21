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


def check_robot_txt(url):

    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    system_instruction = """
    From the given robots.txt text string, identify if webstracping is allowed on a website.

    What you need to provide is a string that is either "Allowed" or "Not Allowed".
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

    return (response.text)
