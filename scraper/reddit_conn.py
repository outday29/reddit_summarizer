import praw

from .settings import settings

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=settings.personal_use_script,
    client_secret=settings.client_secret,
    user_agent=settings.user_agent,
    username=settings.username,
    password=settings.password,
)
