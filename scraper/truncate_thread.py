import logging
import warnings
from datetime import datetime
from pathlib import Path

import praw
import yaml

from scraper.models import CommentsFilter


def truncate_thread(
    submission_object: praw.models.reddit.submission.Submission,
    comment_rules: CommentsFilter,
    output_path: Path,
):
    # Get submission details
    title = submission_object.title
    votes = submission_object.score
    op = submission_object.author.name
    content = submission_object.selftext
    posted_time = datetime.utcfromtimestamp(submission_object.created_utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    link = submission_object.permalink
    # tags = [t['name'] for t in submission_object.subreddit['tags']]
    tags = []

    def is_comment(obj):
        return not isinstance(obj, praw.models.MoreComments)

    # Get top comments
    comments = []
    top_comments = filter(is_comment, submission_object.comments)
    top_comments = sorted(top_comments, key=lambda c: c.score, reverse=True)[
        : comment_rules.comments_top
    ]

    # logging.debug("Top comments:")
    # for comment in top_comments:
    #     logging.debug(f"{comment.author.name} - {comment.score}")
    # input()

    for comment in top_comments:
        if (comment_rules.comment_min_votes != -1) and (
            comment.score < comment_rules.comment_min_votes
        ):
            continue

        comment_dict = {
            "username": comment.author.name if comment.author else "No Author",
            "votes": comment.score,
            "text": comment.body,
        }
        if comment_rules.max_replies_level > 0:
            comment_dict["replies"] = _get_comment_replies(
                comment,
                comment_rules.max_replies,
                comment_rules.max_replies_level - 1,
                comment_rules.reply_min_votes,
            )
        comments.append(comment_dict)

    # Create summary dict
    summary_dict = {
        "title": title,
        "votes": votes,
        "op": op,
        "content": content,
        "posted_time": posted_time,
        "link": link,
        "tags": tags,
        "comments": comments,
    }

    # Write summary to YAML file
    with open(output_path / f"{submission_object.id}.yaml", "w", encoding="utf8") as f:
        yaml.dump(summary_dict, f)


def _get_comment_replies(comment, max_replies, max_level, min_votes):
    replies = []

    def is_comment(obj):
        return not isinstance(obj, praw.models.MoreComments)

    top_replies = filter(is_comment, comment.replies)
    top_replies = sorted(top_replies, key=lambda c: c.score, reverse=True)[:max_replies]

    for reply in top_replies:
        if (min_votes != -1) and (reply.score < min_votes):
            continue

        reply_dict = {
            "username": reply.author.name,
            "votes": reply.score,
            "text": reply.body,
        }
        if max_level > 0:
            reply_dict["replies"] = _get_comment_replies(
                reply, max_replies, max_level - 1, min_votes
            )
        replies.append(reply_dict)
    return replies
