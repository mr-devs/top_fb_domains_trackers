"""
Purpose: 
    - This script extracts top entities from both the below accounts that 
        were scraped with earlier scripts in the pipeline:
        - @FacebooksTop10
    	- @citizenbrowser (Trending on Facebook)

Inputs:
    - The account file to clean.

Outputs:
    - A .jsonl file that contains all of the user data where each row is one
    of the two users.

Author: Matthew DeVerna
"""
import argparse
import datetime
import json

from dateutil import parser
import pickle as pkl

from collections import defaultdict

OUTPUT_NAME_FB_TEN = "fb_top_ten_entities_by_month"
OUTPUT_NAME_CITIZEN_BROWSER = "citizen_browser_entities_by_month"
OUTPUT_DATE_STR = "%Y-%m-%d"

SCRIPT_PURPOSE = (
    "This script cleans the account data output by twarc2. Specifically, "
    "it converts the json data objects into a clean csv. Just provide "
    "the full path to the file you'd like to clean."
)


def parse_cl_args():
    """Set CLI Arguments."""
    print("Attempting to parse command line arguments...")

    try:
        # Initialize parser
        parser = argparse.ArgumentParser(
            description=SCRIPT_PURPOSE,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Add arguments
        arg_text = (
            "Full path to this account's tweet data. "
            "Should be the flattened .jsonl file."
        )
        parser.add_argument(
            "--fb-top-ten-file",
            metavar="File to FacebooksTop10 tweet data",
            help=arg_text,
            required=True,
        )

        parser.add_argument(
            "--citizen-browser-file",
            metavar="File to citizenbrowsers tweet data",
            help=arg_text,
            required=True,
        )

        # Read parsed arguments from the command line into "args"
        args = parser.parse_args()
        print("Success.")
        return args

    except Exception as e:
        print("Problem parsing command line input.")
        print(e)


def is_fbtopten_tweet_i_want(tweet_text):
    """
    Check that the tweet contains all top ten positions.

    Parameter:
    ----------
    - text_tweet (str) : the tweet text

    Return:
    ----------
    - output (bool) : whether it is a tweet we want or not
    """
    ranks = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."]
    return any(rank in tweet_text for rank in ranks)


def get_fb_top_ten(tweet_text):
    """
    Extract the top ten reported by fbtopten account.

    Parameter:
    ----------
    - text_tweet (str) : the tweet text

    Return:
    ----------
    - topten (list) : the entities that have been extracted
    """
    ranks = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."]

    topten = []
    for obj in tweet_text.split("\n"):
        for rank in ranks:
            if obj.startswith(rank):
                replaceme = f"{rank} "
                topten.append(obj.replace(replaceme, ""))

    return topten

def is_citizenbrowser_tweet_i_want(tweet_text):
    """
    Check that the tweet contains top position emojis that
    identify our top ranking tweets.
    
    text_tweet (str) : the tweet text
    
    output (bool) : whether it is a tweet we want or not
    """
    # Manually convert emoji character to bytes
    one_emoji_bstring = bytes('1️⃣', 'utf-8')
    two_emoji_bstring = bytes('2️⃣', 'utf-8')
    three_emoji_bstring = bytes('3️⃣', 'utf-8')
    four_emoji_bstring = bytes('4️⃣', 'utf-8')
    five_emoji_bstring = bytes('5️⃣', 'utf-8')
    all_emojis = [
        one_emoji_bstring,
        two_emoji_bstring,
        three_emoji_bstring,
        four_emoji_bstring,
        five_emoji_bstring
    ]
    # Easier to match emojis with their byte strings
    tweet_text_bytes = bytes(tweet_text, 'utf-8')
    return any(rank in tweet_text_bytes for rank in all_emojis)

def get_citizenbrowser_top_five(tweet_text):
    """
    Extract the top ranked by citizenbrowser account.

    Parameter:
    ----------
    - text_tweet (str) : the tweet text

    Return:
    ----------
    - topranked (list) : the entities that have been extracted
    """
    # CitizenBrowser user these emojis as their rank identifiers
    # we match to these below.
    one_emoji_bstring = bytes('1️⃣', 'utf-8')
    two_emoji_bstring = bytes('2️⃣', 'utf-8')
    three_emoji_bstring = bytes('3️⃣', 'utf-8')
    four_emoji_bstring = bytes('4️⃣', 'utf-8')
    five_emoji_bstring = bytes('5️⃣', 'utf-8')
    all_emojis = [
        one_emoji_bstring,
        two_emoji_bstring,
        three_emoji_bstring,
        four_emoji_bstring,
        five_emoji_bstring
    ]
    
    topranked = []
    
    for obj in tweet_text.split('\n'):
        for rank in all_emojis:
            # Convert to byte-string before attempting to match
            byte_obj = bytes(obj, 'utf-8')
            if byte_obj.startswith(rank):
                try:
                    topranked.append( obj.split(" ")[1] )
                
                # Sometimes the rank position is included without a URL
                except:
                    print("One of the ranks was not reported. Skipping...")
    
    return topranked

if __name__ == "__main__":

    # Parse needed command-line info
    args = parse_cl_args()
    fb_top_ten_file = args.fb_top_ten_file
    citizen_browser_file = args.citizen_browser_file

    both_files = [fb_top_ten_file, citizen_browser_file]
    if any ('flattened' not in fp for fp in both_files):
        raise ValueError("Input files must be 'flattened' .jsonl format.")

    print("\n\n\nProcessing @FacebooksTopTen tweets...")
    print("-"*50)
    tweets = []
    with open(fb_top_ten_file, "r") as f:
        for line in f:
            tweet = json.loads(line)
            tweets.append(tweet)

    fb_top_ten_all_data = defaultdict(list)

    for tweet in tweets:
        tweet_text = tweet["text"]

        if not is_fbtopten_tweet_i_want(tweet_text):
            print('-'*10)
            print('Tweet skipped...')
            print(tweet_text)
            print(f"Tweet ID: {tweet['id']}")
            print('-'*10)
            continue

        created_dt = parser.isoparse(tweet["created_at"])
        date_key = created_dt.strftime("%Y_%m")

        try:
            top_ten = get_fb_top_ten(tweet_text)
        except:
            print("Ran into a problem parsing the top ten. Skipping the below tweet...")
            print("-" * 10)
            print(tweet_text)
            print(f"Tweet ID: {tweet['id']}")
            print("-" * 10)

        fb_top_ten_all_data[date_key].extend(top_ten)

    # Convert defaultdict to regular dict
    fb_top_ten_all_data = dict(fb_top_ten_all_data)

    today_dt_obj = datetime.datetime.today()
    today_date_str = datetime.datetime.strftime(today_dt_obj, OUTPUT_DATE_STR)
    fb_full_output_name = f"{OUTPUT_NAME_FB_TEN}_{today_date_str}.pkl"
    with open(fb_full_output_name, "wb") as f:
        pkl.dump(
            fb_top_ten_all_data,
            f,
            protocol=pkl.HIGHEST_PROTOCOL
            )

    print("\n\n\nCOMPLETE", "-" * 50)

    print("\n\n\nProcessing @citizenbrowser tweets...")
    print("-"*50)
    tweets = []
    with open(citizen_browser_file, "r") as f:
        for line in f:
            tweet = json.loads(line)
            tweets.append(tweet)

    cb_top_five_all_data = defaultdict(list)

    for tweet in tweets:
        tweet_text = tweet['text']
        
        if not is_citizenbrowser_tweet_i_want(tweet_text):
            print(tweet_text)
            print(tweet['id'])
            continue

        created_dt = parser.isoparse(tweet['created_at'])
        date_key = created_dt.strftime("%Y_%m")
        
        try:
            top_ten = get_citizenbrowser_top_five(tweet_text)
        except:
            print("Ran into a problem parsing the top ranked. Skipping the below tweet...")
            print("-"*50)
            print(tweet_text)
            print("-"*50)
        
        cb_top_five_all_data[date_key].extend(top_ten)
    
    cb_full_output_name = f"{OUTPUT_NAME_CITIZEN_BROWSER}_{today_date_str}.pkl"
    with open(cb_full_output_name, "wb") as f:
        pkl.dump(
            cb_top_five_all_data,
            f,
            protocol=pkl.HIGHEST_PROTOCOL
            )
    
    print("\n\n\nCOMPLETE", "-" * 50)
    print("-- script complete ---")