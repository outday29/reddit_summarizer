import datetime
from pathlib import Path

from benedict import benedict

from scraper.models import CommentsFilter, ThreadsFilter
from scraper.scrape_subreddit import scrape_subreddit
from scraper.summarize_thread import summarize_thread
from scraper.truncate_thread import truncate_thread


def summarize():
    interest_config = benedict.from_yaml("interest.yaml")
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filtered_output_path = Path("./filtered") / current_time
    report_output_path = Path("./report/") / current_time

    for subreddit in interest_config.subreddits:
        cur_output_path = filtered_output_path / subreddit.name
        cur_output_path.mkdir(exist_ok=True, parents=True)
        filter_rules_list = [ThreadsFilter(**rules) for rules in subreddit.threads]
        threads_list = scrape_subreddit(
            subreddit.name, filter_rules_list=filter_rules_list
        )
        comment_filter_rules = CommentsFilter(**subreddit.comments)
        for thread in threads_list:
            truncate_thread(
                submission_object=thread,
                comment_rules=comment_filter_rules,
                output_path=cur_output_path,
            )

    subreddit_list = [i for i in filtered_output_path.iterdir() if i.is_dir()]
    for subreddit in subreddit_list:
        for thread in subreddit.iterdir():
            cur_output_path = report_output_path / subreddit.name
            cur_output_path.mkdir(exist_ok=True, parents=True)
            summarize_thread(thread, output_path=cur_output_path / thread.name)


if __name__ == "__main__":
    summarize()
