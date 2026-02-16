#!/usr/bin/python3
"""
0-subs.py

Provides a function to return the total number of subscribers for a
given subreddit using Reddit's public API. Returns 0 for invalid
subreddits.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Return the number of subscribers for the given subreddit.
    If invalid, return 0.
    """
    if not subreddit or not isinstance(subreddit, str):
        return 0

    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "ALU-API-Advanced/1.0"}
    try:
        resp = requests.get(
            url, headers=headers, allow_redirects=False, timeout=10
        )
    except requests.RequestException:
        return 0

    if resp.status_code != 200:
        return 0

    try:
        data = resp.json().get("data", {})
    except ValueError:
        return 0

    return data.get("subscribers", 0)
