#!/usr/bin/python3
"""
Module that queries the Reddit API and prints the titles of the first
10 hot posts listed for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit.
    """
    # A custom User-Agent is REQUIRED to avoid 429 Too Many Requests errors
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {'limit': 10}

    try:
        # allow_redirects=False is CRITICAL.
        # Invalid subreddits redirect to a search page (status 302/200).
        # We must stop the redirect to catch the invalid status.
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        # Only proceed if the status is exactly 200 OK
        if response.status_code == 200:
            data = response.json().get("data")
            children = data.get("children")
            for child in children:
                print(child.get("data").get("title"))
        else:
            # If status is 302 (redirect) or 404 (not found), print None
            print("None")
    except Exception:
        print("None")
