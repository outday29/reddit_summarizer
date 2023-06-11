from typing import List, Optional

from pydantic import BaseModel


class ThreadsFilter(BaseModel):
    votes: int = 0
    num_comments: int = 0
    upvote_ratio: float = 0.0
    recency: Optional[int] = None
    limit: int = 0


class CommentsFilter(BaseModel):
    comments_top: int = 0
    comment_min_votes: int = 0
    reply_min_votes: int = 0
    max_replies: int = 0
    max_replies_level: int = 0


class Subreddit(BaseModel):
    name: str
    threads: List[ThreadsFilter]
    comments: CommentsFilter


class Summary(BaseModel):
    title: str
    link: str
    user: str
    description: str
