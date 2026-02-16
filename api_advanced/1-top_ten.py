#!/usr/bin/python3
"""
1-top_ten.py

Prints the titles of the first 10 hot posts for a given subreddit.
Prints 'None' if the subreddit is invalid.
"""
import requests


def top_ten(subreddit):
    """
    Print the titles of the first 10 hot posts.
    If invalid, print 'None'.
    """
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "ALU-API-Advanced/1.0"}
    params = {"limit": 10}

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
        print("None")
        return

    if resp.status_code != 200:
        print("None")
        return

    try:
        children = resp.json().get("data", {}).get("children", [])
    except ValueError:
        print("None")
        return

    if not children:
        print("None")
        return

    for post in children:
        title = post.get("data", {}).get("title")
        if title is not None:
            print(title)
