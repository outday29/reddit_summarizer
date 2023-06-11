## Overview

`reddit_summarizer` summarizes subreddit threads using OpenAI GPT 3.5.

## Usage

First, clone this repository into your system.

```bash
git clone https://github.com/outday29/reddit_summarizer
```

Install necessary dependencies

```bash
pip install -r requirements.txt
```

Create a Python script called `secret.py` in the top directory. In the Python script, define the following constants:

```python
PERSONAL_USE_SCRIPT="your_reddit_use_script"
CLIENT_SECRET="your_reddit_client_secret"
USER_AGENT="your_reddit_user_agent"
USERNAME="your_reddit_username"
PASSWORD="your_reddit_pwd"
OPENAI_KEY="your_openai_key" # Used for querying gpt-3.5 turbo
```

Then specify what subreddits to summarize by configuring `interest.yaml` (You can look at the example). You can also specify what comments to keep or filtered out during summarization.

Below is the explanation for each field:

```yaml
subreddits: 
# Define a list of settting objects, each specifies one subreddit
  - name: ChatGPT # What is the name of the subreddit to scrape?
    threads: 
    # Define a list of thread-specific rules to select which threads in the subreddit to summarize.
    # Any thread that satisfies any of the rules will be included.
    - limit: 5 # Number of threads to select at most
      recency: 7 # Only select threads that are created less than 7 days ago
      num_comments: 10 # Minimum number of comments the threads need to have
      upvote_ratio: 0.5 # Minimum upvote_ratio for the thread to be selected
      votes: 100 # Minimum amount of upvotes threads should have
    comments:
    # For selected threads, specify how should we filter the comments. 
      comments_top: 10 # Select the top 10 comments
      comment_min_votes: 100 # Minimum number of upvotes comments should have.
      reply_min_votes: 5 # How many upvotes a reply should have to be selected
      max_replies: 5 # Maximum number of replies to be selected for each depth level.
      max_replies_level: 2 # Only select nested replies (replies to reply) of depth of 2. Reply to comments has depth of 1. In this case, we only select reply to comments + the repiesy to replies to comments.
```

Then run the following command to scrape and summarize the subreddits defined just now.

```
python main.py
```

You may then view the summary in a nice Streamlit UI.

```
streamlit run main.py
```
