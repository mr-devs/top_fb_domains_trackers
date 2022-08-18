"""
Purpose: 
    - This script cleans the account data output by twarc2. Specifically,
    it converts the json data objects into a clean csv.

Inputs:
    - The account file to clean.

Outputs:
    - A .csv file that contains all of the user data where each row is one
    of the two users.

Author: Matthew DeVerna
"""
import argparse
import datetime
import json

import pandas as pd

from osometweet.wrangle import get_dict_val

OUTPUT_NAME = "account_data_clean"
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
        parser.add_argument(
            "-f",
            "--file",
            metavar="File to Clean",
            help="Full path to the file that you want to clean",
            required=True,
        )

        # Read parsed arguments from the command line into "args"
        args = parser.parse_args()
        print("Success.")
        return args

    except Exception as e:
        print("Problem parsing command line input.")
        print(e)


if __name__ == "__main__":

    # Parse needed command-line info
    args = parse_cl_args()
    account_info_fp = args.file

    with open(account_info_fp, "r") as f:
        for line in f:
            data = json.loads(line)

    clean_info = []

    for user in data["data"]:
        username = get_dict_val(user, ["username"])
        verified = get_dict_val(user, ["verified"])
        name = get_dict_val(user, ["name"])
        account_id = get_dict_val(user, ["id"])
        description = get_dict_val(user, ["description"])
        created_at = get_dict_val(user, ["created_at"])
        location = get_dict_val(user, ["location"])
        followers_count = get_dict_val(user, ["public_metrics", "followers_count"])
        following_count = get_dict_val(user, ["public_metrics", "following_count"])
        tweet_count = get_dict_val(user, ["public_metrics", "tweet_count"])
        listed_count = get_dict_val(user, ["public_metrics", "listed_count"])
        pinned_tweet_id = get_dict_val(user, ["pinned_tweet_id"])
        profile_image_url = get_dict_val(user, ["profile_image_url"])
        url = get_dict_val(user, ["url"])
        protected = get_dict_val(user, ["protected"])

        clean_info.append(
            (
                username,
                verified,
                name,
                account_id,
                description,
                created_at,
                location,
                followers_count,
                following_count,
                tweet_count,
                listed_count,
                pinned_tweet_id,
                profile_image_url,
                url,
                protected,
            )
        )

    clean_account_frame = pd.DataFrame(
        clean_info,
        columns=[
            "username",
            "verified",
            "name",
            "account_id",
            "description",
            "created_at",
            "location",
            "followers_count",
            "following_count",
            "tweet_count",
            "listed_count",
            "pinned_tweet_id",
            "profile_image_url",
            "url",
            "protected",
        ],
    )

    today_dt_obj = datetime.datetime.today()
    today_date_str = datetime.datetime.strftime(today_dt_obj, OUTPUT_DATE_STR)
    full_output_name = f"{OUTPUT_NAME}_{today_date_str}.csv"
    clean_account_frame.to_csv(full_output_name)
    print("--- script complete ---")
