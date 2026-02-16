#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first
10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a given subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    # Use a clear, specific User-Agent Reddit will accept
    headers = {"User-Agent": "python:api_advanced.topten:v1.0 (by /u/solomon)"}
    params = {"limit": 10}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10,
        )

        # Invalid subreddit or blocked request (e.g., 301/302/403/404/429)
        if response.status_code != 200:
            print("None")
            return

        data = response.json().get("data", {})
        children = data.get("children", [])

        if not children:
            print("None")
            return

        for post in children:
            title = post.get("data", {}).get("title")
            if title is not None:
                print(title)

    except Exception:
        print("None")
