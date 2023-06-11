from typing import List

import attrs


@attrs.define
class ThreadsFilter:
    votes: int = -1
    num_comments: int = -1
    upvote_ratio: float = -1
    recency: int = -1
    limit: int = -1


@attrs.define
class CommentsFilter:
    comments_top: int = -1
    comment_min_votes: int = -1
    reply_min_votes: int = -1
    max_replies: int = -1
    max_replies_level: int = -1


@attrs.define
class Subreddit:
    name: str
    threads: List[ThreadsFilter]
    comments: CommentsFilter


@attrs.define
class Summary:
    title: str
    link: str
    user: str
    description: str
