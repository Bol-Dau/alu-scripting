#!/usr/bin/python3
"""
2-recurse.py

Recursively queries Reddit's API to return a list containing the titles
of all hot posts for a given subreddit. Returns None if invalid.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Return a list of all hot post titles for the subreddit.
    If invalid, return None.

    This function is recursive: it requests a page, appends titles,
    then calls itself with the next 'after' until there is no more.
    """
    if hot_list is None:
        hot_list = []

    if not subreddit or not isinstance(subreddit, str):
        return None

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "ALU-API-Advanced/1.0"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    try:
        data = resp.json().get("data", {})
    except ValueError:
        return None

    children = data.get("children", [])
    for post in children:
        title = post.get("data", {}).get("title")
        if title is not None:
            hot_list.append(title)

    next_after = data.get("after")
    if next_after:
        return recurse(subreddit, hot_list, next_after)

    return hot_list
