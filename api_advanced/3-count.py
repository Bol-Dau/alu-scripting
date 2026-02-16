#!/usr/bin/python3
"""
3-count.py

Recursively queries Reddit's API for all hot post titles of a subreddit
and prints a sorted count of given keywords.

Rules:
- Case-insensitive matching.
- Exact token match (space-delimited); do not match substrings.
- Do not count tokens like 'java.' or 'java!' as 'java'.
- Duplicate keywords in word_list multiply the final count.
- Print nothing if subreddit is invalid or there are no matches.
"""
import requests


def count_words(subreddit, word_list):
    """
    Print the keyword counts in descending order by count, then A–Z.
    Words are printed in lowercase; words with zero matches are skipped.
    """
    if not subreddit or not isinstance(subreddit, str):
        return

    if not word_list:
        return

    # Normalize word_list to lowercase and aggregate duplicate weights.
    weights = {}
    for w in word_list:
        lw = w.lower()
        if lw:
            weights[lw] = weights.get(lw, 0) + 1

    # Internal recursive helper to gather counts across pages.
    def _recurse(after=None, counts=None):
        if counts is None:
            counts = {}

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

        # Count exact token matches (space-delimited) without stripping
        # punctuation, as required.
        for post in children:
            title = post.get("data", {}).get("title", "")
            tokens = [t.lower() for t in title.split()]
            for word in weights.keys():
                # Count occurrences of the exact word among tokens.
                occ = sum(1 for t in tokens if t == word)
                if occ:
                    counts[word] = counts.get(word, 0) + occ

        next_after = data.get("after")
        if next_after:
            return _recurse(next_after, counts)

        return counts

    counts = _recurse(after=None, counts={})
    if counts is None:
        # Invalid subreddit or request error -> print nothing
        return

    # Multiply by duplicate weights and filter zeros
    final = {}
    for word, weight in weights.items():
        total = counts.get(word, 0) * weight
        if total > 0:
            final[word] = total

    if not final:
        # No matches -> print nothing
        return

    # Sort by (-count, word) and print
    for word, total in sorted(final.items(), key=lambda x: (-x[1], x[0])):
        print(f"{word}: {total}")
