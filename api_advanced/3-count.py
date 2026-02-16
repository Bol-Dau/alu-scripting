#!/usr/bin/python3
"""
Recursive function that queries the Reddit API,
parses hot article titles, and counts given keywords.
"""
import requests


def count_words(subreddit, word_list, hot_list=None, after=None, counts=None):
    """
    Recursively count occurrences of words in all hot post titles.
    Prints results sorted by descending count and alphabetically.
    """
    if hot_list is None:
        hot_list = []
    if counts is None:
        counts = {}

    # Prepare URL and headers
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:api_advanced:v1.0 (by /u/solomon)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            params=params
        )
        if response.status_code != 200:
            if counts:
                _print_counts(counts)
            return

        data = response.json().get("data", {})
        children = data.get("children", [])
        for post in children:
            title = post.get("data", {}).get("title", "").lower()
            for word in word_list:
                word_lc = word.lower()
                # Count exact whole words only (split by spaces)
                current_count = counts.get(word_lc, 0)
                counts[word_lc] = current_count + title.split().count(word_lc)

        after = data.get("after")
        if after:
            # Recursive call for next page
            count_words(subreddit, word_list, hot_list, after, counts)
        else:
            # No more pages, print counts
            _print_counts(counts)

    except Exception:
        # Do nothing if subreddit is invalid or request fails
        return


def _print_counts(counts):
    """Helper function to print counts sorted by requirements"""
    # Remove words with 0 occurrences
    filtered = {k: v for k, v in counts.items() if v > 0}
    if not filtered:
        return
    # Sort: descending by count, then alphabetically
    sorted_counts = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print("{}: {}".format(word, count))
