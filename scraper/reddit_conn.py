import praw

from secret import CLIENT_SECRET, PASSWORD, PERSONAL_USE_SCRIPT, USER_AGENT, USERNAME

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=PERSONAL_USE_SCRIPT,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD,
)
