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
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_pla)"
    }
    params = {
        "limit": 10
    }
    
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    
    if response.status_code == 404:
        print("None")
        return

    if response.status_code != 200:
        print("None")
        return

    try:
        results = response.json().get("data").get("children")
        for child in results:
            print(child.get("data").get("title"))
    except Exception:
        print("None")
