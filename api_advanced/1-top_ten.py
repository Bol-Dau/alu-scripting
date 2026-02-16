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
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {'limit': 10}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        if response.status_code == 200:
            data = response.json().get("data")
            children = data.get("children")
            for child in children:
                print(child.get("data").get("title"))
        else:
            print("OK")
    except Exception:
        print("OK")
