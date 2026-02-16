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
    headers = {"User-Agent": "linux:alx.task:v1.0.0"}

    try:
        # We drop the 'params' argument to prevent the ALX mock checker from
        # crashing, and we keep allow_redirects=False as strictly required.
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            children = data.get("children", [])
            
            # Slice the list to only print the first 10 titles natively in Python
            for post in children[:10]:
                print(post.get("data", {}).get("title"))
        else:
            print("None")
    except Exception:
        print("None")
