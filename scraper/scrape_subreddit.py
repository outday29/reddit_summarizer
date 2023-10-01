from datetime import datetime
from typing import List

import praw

from scraper.models import PostFilter
from scraper.reddit_conn import reddit


def scrape_subreddit(
    subreddit_name: str, filter_rules_list: List[PostFilter]
) -> List:
    """
    Returns all posts in a subreddit that match all the rules specified in PostFilter.

    Args:
    subreddit_name (str): Name of the subreddit to scrape.
    filter_rules_list (List[PostFilter]): List of PostFilter objects.

    Returns:
    List: List of praw.models.reddit.submission.Submission objects.
    """
    # Get subreddit instance
    subred = reddit.subreddit(subreddit_name)

    # Initialize list to store filtered posts
    filtered_posts = []

    # Iterate through each set of filter rules
    for filter_rules in filter_rules_list:
        # Get top 100 hot posts in subreddit
        cur_result = subred.hot(limit=100)

        # Filter posts that match the current set of rules
        cur_result = [
            t for t in cur_result if _post_matches_filter_rules(t, filter_rules)
        ]

        # Apply limit if specified in filter_rules
        if len(cur_result) > filter_rules.limit:
            cur_result = cur_result[: filter_rules.limit]

        # Add filtered posts to the list
        filtered_posts.extend(cur_result)

    return filtered_posts


def _post_matches_filter_rules(
    post: praw.models.reddit.submission.Submission, rule: PostFilter
):
    """
    Check if a post matches all the rules specified in filter_rules.

    Args:
    post (praw.models.reddit.submission.Submission): Reddit submission/post object.
    filter_rules (FilterRules): FilterRules object.

    Returns:
    bool: True if post matches all rules, False otherwise.
    """
    # Check popularity rule
    if post.score < rule.votes:
        return False

    # Check recency rule
    if rule.recency is not None:
        age = (datetime.utcnow() - datetime.utcfromtimestamp(post.created_utc)).days
        if age > rule.recency:
            return False

    if post.num_comments < rule.num_comments:
        return False

    if post.upvote_ratio < rule.upvote_ratio:
        return False

    # Check tags_include rule
    # if rule.tags_include:
    #     has_include_tags = False
    #     for tag in rule.tags_include:
    #         if tag in post.title.lower():
    #             has_include_tags = True
    #             break
    #     if not has_include_tags:
    #         return False

    # # Check tags_exclude rule
    # if rule.tags_exclude:
    #     has_exclude_tags = False
    #     for tag in rule.tags_exclude:
    #         if tag in post.title.lower():
    #             has_exclude_tags = True
    #             break
    #     if has_exclude_tags:
    #         return False

    return True
