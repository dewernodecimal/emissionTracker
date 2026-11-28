from google import genai          # Google Gemini library
import time                       # for retry waits
import os                         # to read environment variables
from dotenv import load_dotenv    # to load the .env file

load_dotenv()   # reads the .env file and loads the variables into the environment

# API key is now read from .env file — never hardcoded here
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)   # connect to Google's servers


def classify_dataset(df):


    #take only the first 5 rows 
    sample = df.head(5)

    #convert the dataframe to plain text so Gemini can read it like a table
    sample_text = sample.to_string(index=False)

    # get just the column names as a comma-separated string
    column_names = ", ".join(df.columns.tolist())


    # prompt for gemini — now supports multiple categories in one file
    prompt = f"""
You are a carbon emission data classifier.

A company has uploaded a data file. Your job is to look at the column names
and a few sample rows, then decide which categories this data belongs to.

The possible categories are:
- "Travel"  → data about business trips: flights, hotels, trains, rental cars
- "Commute" → data about employees travelling to/from work: cars, buses, metro, bikes
- "Waste"   → data about waste disposal: landfill, recycling, composting, incineration

Here are the column names from the file:
{column_names}

Here are the first few rows of data:
{sample_text}

Rules:
- If the file contains only ONE type of data, reply with just that one word. Example: Travel
- If the file contains a MIX of multiple types, reply with all that apply separated by commas. Example: Travel, Commute
- If you cannot tell at all, reply with: Unknown
- Do not explain. Do not add punctuation beyond commas. Just the category words.
"""

    # send the prompt to Gemini — retry up to 3 times if the server is busy
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",    # the model to use
                contents=prompt
            )
            break    # if it worked, exit the retry loop

        except Exception as e:
            if attempt < 2:                           # if we still have retries left
                time.sleep(3)                         # wait 3 seconds before trying again
            else:
                raise e                               # on the 3rd failure, give up and raise the error

    # pull the text out of the response and clean up whitespace
    raw = response.text.strip()

    # split by comma in case multiple categories were returned (e.g. "Travel, Commute")
    parts = [p.strip().capitalize() for p in raw.split(",")]

    valid = {"Travel", "Commute", "Waste", "Unknown"}   # set of valid answers

    # keep only the parts that are valid category names
    matched = [p for p in parts if p in valid]

    if not matched:
        return "Unknown"   # nothing matched — fall back to Unknown

    # if multiple categories found, join them back as a string e.g. "Travel, Waste"
    return ", ".join(matched)
