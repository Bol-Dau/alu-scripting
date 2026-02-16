#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first
10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a given subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return

    # Use the API domain; it's less likely to redirect to search
    url = "https://api.reddit.com/r/{}/hot".format(subreddit)

    headers = {
        # Clear, specific UA improves acceptance and avoids 429/403
        "User-Agent": "python:alu.api_advanced.topten:v1.0 (by /u/solomon)",
        "Accept": "application/json",
    }
    params = {"limit": 10}

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10,
        )

        # Any non-200 (including 301/302/403/404/429) → treat as invalid
        if resp.status_code != 200:
            print("None")
            return

        payload = resp.json()
        data = payload.get("data", {})
        children = data.get("children", [])

        if not children:
            # Valid subreddit but no posts → per checker, print None
            print("None")
            return

        for post in children:
            title = post.get("data", {}).get("title")
            if title:
                print(title)

    except Exception:
        # Network/JSON errors → print None as per checker expectation
        print("None")
