#!/usr/bin/python3
"""
Recursive function that queries the Reddit API and returns
a list of all hot article titles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Recursively retrieves all hot article titles for a subreddit."""
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:api_advanced:v1.0 (by /u/solomon)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers,
                                allow_redirects=False, params=params)
        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        children = data.get("children", [])
        for post in children:
            hot_list.append(post.get("data", {}).get("title"))

        after = data.get("after")
        if after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, after)

    except Exception:
        return None
