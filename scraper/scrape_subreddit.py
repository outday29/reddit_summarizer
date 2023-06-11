from datetime import datetime
from typing import List

import praw

from scraper.models import ThreadsFilter
from scraper.reddit_conn import reddit


def scrape_subreddit(
    subreddit_name: str, filter_rules_list: List[ThreadsFilter]
) -> List:
    """
    Returns all threads in a subreddit that match all the rules specified in ThreadsFilter.

    Args:
    subreddit_name (str): Name of the subreddit to scrape.
    filter_rules_list (List[ThreadsFilter]): List of ThreadsFilter objects.

    Returns:
    List: List of praw.models.reddit.submission.Submission objects.
    """
    # Get subreddit instance
    subred = reddit.subreddit(subreddit_name)

    # Initialize list to store filtered threads
    filtered_threads = []

    # Iterate through each set of filter rules
    for filter_rules in filter_rules_list:
        # Get top 100 hot threads in subreddit
        cur_result = subred.hot(limit=100)

        # Filter threads that match the current set of rules
        cur_result = [
            t for t in cur_result if _thread_matches_filter_rules(t, filter_rules)
        ]

        # Apply limit if specified in filter_rules
        if (filter_rules.limit != -1) and (len(cur_result) > filter_rules.limit):
            cur_result = cur_result[: filter_rules.limit]

        # Add filtered threads to the list
        filtered_threads.extend(cur_result)

    return filtered_threads


def _thread_matches_filter_rules(
    thread: praw.models.reddit.submission.Submission, rule: ThreadsFilter
):
    """
    Check if a thread matches all the rules specified in filter_rules.

    Args:
    thread (praw.models.reddit.submission.Submission): Reddit thread object.
    filter_rules (FilterRules): FilterRules object.

    Returns:
    bool: True if thread matches all rules, False otherwise.
    """
    # Check popularity rule
    if rule.votes != -1:
        # Check if thread score is less than specified votes
        if thread.score < rule.votes:
            return False

    # Check recency rule
    if rule.recency != -1:
        age = (datetime.utcnow() - datetime.utcfromtimestamp(thread.created_utc)).days
        if age > rule.recency:
            return False

    if rule.num_comments != -1:
        if thread.num_comments < rule.num_comments:
            return False

    if rule.upvote_ratio != -1:
        if thread.upvote_ratio < rule.upvote_ratio:
            return False

    # Check tags_include rule
    # if rule.tags_include:
    #     has_include_tags = False
    #     for tag in rule.tags_include:
    #         if tag in thread.title.lower():
    #             has_include_tags = True
    #             break
    #     if not has_include_tags:
    #         return False

    # # Check tags_exclude rule
    # if rule.tags_exclude:
    #     has_exclude_tags = False
    #     for tag in rule.tags_exclude:
    #         if tag in thread.title.lower():
    #             has_exclude_tags = True
    #             break
    #     if has_exclude_tags:
    #         return False

    return True
