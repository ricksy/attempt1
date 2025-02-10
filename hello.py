#!/usr/bin/env -S uv run --script
import os
from atproto import Client
import random
import json
import glob
import time
import schedule
def main():


    def job():
        random_quote_text, random_quote_author = get_quote()
        if not random_quote_text or not random_quote_author:
            raise ValueError("The selected quote does not contain both 'text' and 'author' fields")
        QotD = random_quote_text + " - " + random_quote_author
        print("random quote of the day: " + random_quote_text + " - " + random_quote_author)
        # Call the function with the quote of the day
        post_2_bluesky(QotD)

    # Execute once when the script starts
    job()

    # Schedule the job every day at 8 AM CET
    schedule.every().day.at("08:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def get_quote():
    # Get a list of all JSON files in the directory
    json_files = glob.glob('./short-quotes/en/*.json')

    if not json_files:
        raise FileNotFoundError("No JSON files found in the directory")

    # Pick a random JSON file
    random_file = random.choice(json_files)

    # Read the content of the random JSON file
    with open(random_file, 'r') as file:
        quotes = json.load(file)

    if not quotes:
        raise ValueError("The selected JSON file is empty")

    # Pick a random line from the JSON file
    random_quote = random.choice(quotes)
    random_quote_author = random_quote.get('author')
    random_quote_text = random_quote.get('text')

    return random_quote_text, random_quote_author
def post_2_bluesky(content):
    client = Client()
    
    username = os.getenv('BSKY_USERNAME')
    password = os.getenv('BSKY_PASSWORD')
    
    if not username or not password:
        raise ValueError("Environment variables BSKY_USERNAME and BSKY_PASSWORD must be set")
    
    client.login(username, password)
    post = client.send_post(content)
    print("happened at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+ " " + post.uri + " " + post.cid)
if __name__ == "__main__":
    main()
