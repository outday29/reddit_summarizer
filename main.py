import datetime
import os
import sys
from pathlib import Path

from benedict import benedict
from loguru import logger

from scraper.models import CommentsFilter, PostFilter
from scraper.scrape_subreddit import scrape_subreddit
from scraper.summarize_post import summarize_post
from scraper.truncate_post import truncate_post

LOG_FILE = "debug.log"
if os.path.isfile(LOG_FILE):
    os.remove(LOG_FILE)

# Configure the logger
logger.remove()
logger.add(sink=sys.stdout, level="INFO")  # Console output with INFO level
logger.add(sink=LOG_FILE, level="DEBUG")  # Debug-level log to a file


def summarize():
    interest_config = benedict.from_yaml("interest.yaml")
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filtered_output_path = Path("./filtered") / current_time
    report_output_path = Path("./report/") / current_time

    logger.info(f"Scraping subreddit...")
    for subreddit in interest_config.subreddits:
        cur_output_path = filtered_output_path / subreddit.name
        cur_output_path.mkdir(exist_ok=True, parents=True)
        filter_rules_list = [PostFilter(**rules) for rules in subreddit.posts]
        logger.debug(f"We have post filter rules of {filter_rules_list}")
        logger.info(
            f"Scraping and filtering subreddit posts for r/{subreddit.name}"
        )
        posts_list = scrape_subreddit(
            subreddit.name, filter_rules_list=filter_rules_list
        )
        comment_filter_rules = CommentsFilter(**subreddit.comments)
        logger.debug(f"We have the comment filter rules of {comment_filter_rules}")
        logger.debug("Filtering post contents")
        for post in posts_list:
            truncate_post(
                submission_object=post,
                comment_rules=comment_filter_rules,
                output_path=cur_output_path,
            )

    subreddit_list = [i for i in filtered_output_path.iterdir() if i.is_dir()]
    logger.info("Summarizing...")
    for subreddit in subreddit_list:
        logger.info(f"Summarizing subreddit {subreddit.name}")
        for post in subreddit.iterdir():
            cur_output_path = report_output_path / subreddit.name
            cur_output_path.mkdir(exist_ok=True, parents=True)
            summarize_post(post, output_path=cur_output_path / post.name)
    logger.info("Done! 🎉")


if __name__ == "__main__":
    summarize()
