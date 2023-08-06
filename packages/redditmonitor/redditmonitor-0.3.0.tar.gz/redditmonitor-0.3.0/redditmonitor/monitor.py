import praw
import requests
import re
import configparser
import logging
import os
import time

def make_client(config, user_agent):
    return praw.Reddit(
        user_agent=user_agent,
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        password=config.get("password"),
        username=config.get("username")
    )

COMMENT_MESSAGE_FMT = """
.
"{body}"

- {author} "[in {submission_title}]({url})"
"""

SUBMISSION_MESSAGE_FMT = """
.
:{emoji}: [{title}]({url})
"""

def safe_send(webhook, content):
    if webhook is not None:
        data = {
            "content": content,
        }
        requests.post(webhook, data=data)

class CommentMonitor():
    def __init__(self, name, config):
        self.logger = logging.getLogger(name)
        self.reddit = make_client(config, user_agent='Expanse Latest Comments to Discord Bot')
        self.subreddit = config["subreddit"]
        self.discord_webhook = config.get("discord_webhook")
        self.spoiler_tag_webhook = config.get("spoiler_tag_webhook")
        self.show_spoiler_flair_webhook = config.get("books_spoiler_flair_webhook")
        self.books_show_spoiler_flair_webhook = config.get("books_show_spoiler_flair_webhook")
        self.no_spoiler_webhook = config.get("no_spoiler_webhook")
        self.no_spoiler_title_webhook = config.get("no_spoiler_title_webhook")

        self.stream = self.reddit.subreddit(self.subreddit).stream.comments(skip_existing=True, pause_after=0)


    def handle_comment(self, comment):
        submission = comment.submission
        self.logger.info("comment received (url: %s, flair: %s, spoilers: %s)", comment.permalink, submission.link_flair_text, submission.spoiler)
        url = "https://www.reddit.com{}?context=9&depth=8".format(comment.permalink)
        content = COMMENT_MESSAGE_FMT.format(url=url, author=comment.author, body=comment.body, submission_title=comment.submission.title)
        safe_send(self.discord_webhook, content)
        if submission.link_flair_text == "All Spoilers (Books and Show)":
            safe_send(self.books_show_spoiler_flair_webhook, content)
        elif submission.link_flair_text == "All Spoilers (Show Only)":
            safe_send(self.show_spoiler_flair_webhook, content)
        elif submission.spoiler:
            safe_send(self.spoiler_tag_webhook, content)
        elif "no spoilers" in submission.title.lower():
            safe_send(self.no_spoiler_title_webhook, content)
        else:
            safe_send(self.no_spoiler_webhook, content)

    def poll(self):
        for comment in self.stream:
           if comment is None:
               return
           self.handle_comment(comment)


class SubmissionMonitor():
    def __init__(self, name, config):
        self.logger = logging.getLogger(name)
        self.reddit = make_client(config, user_agent='Expanse Submissions to Discord Bot')
        self.subreddit = config["subreddit"]
        self.discord_webhook = config.get("discord_webhook")
        self.stream = self.reddit.subreddit(self.subreddit).stream.submissions(skip_existing=True, pause_after=0)

    def handle_submission(self, submission):
        self.logger.info("submission received: (url: %s, flair: %s, spoilers: %s)", submission.permalink, submission.link_flair_text, submission.spoiler)
        if submission.link_flair_text == "All Spoilers (Books and Show)":
            emoji = "bangbang"
        elif submission.link_flair_text == "All Spoilers (Show Only)":
            emoji = "exclamation"
        elif submission.spoiler:
            emoji = "grey_exclamation"
        else:
            emoji = "warning"

        url = "https://www.reddit.com{}".format(submission.permalink)
        content = SUBMISSION_MESSAGE_FMT.format(url=url, author=submission.author, title=submission.title, emoji=emoji)
        safe_send(self.discord_webhook, content)

    def poll(self):
        for submission in self.stream:
           if submission is None:
               return
           self.handle_submission(submission)

class SpoilerMonitor():
    def __init__(self, name, config):
        self.logger = logging.getLogger(name)
        self.reddit = make_client(config, user_agent='Expanse Spoilers Moderator')
        self.subreddit = config["subreddit"]
        self.discord_webhook = config.get("discord_webhook")
        self.spoiler_text = config["spoiler_text"]
        self.stream = self.reddit.subreddit(self.subreddit).stream.submissions(skip_existing=True, pause_after=0)

    def parse_non_spoilers(self, body):
        position = 0
        remaining = body
        current = ""
        while True:
            result = re.search(r">!\S.*?\S!<", remaining)
            if result:
                span = result.span()
                current += remaining[:span[0]]
                remaining = remaining[span[1]:]
            else:
                current += remaining
                break
        return current

    def handle_submission(self, comment):
        self.logger.info("spoiler comment received: %s", comment.permalink)

        spoiler_word = get_spoiler_word(comment)
        if spoiler_word:
            self.logger.info("Spoiler comment!: {}".format(comment))
            comment.report("Automated spoiler alert for word: {}".format(spoiler_word))

    def get_spoiler_word(self, comment):
        if comment.submission.link_flair_text == "All Spoilers (Books and Show)":
            return None
        for spoiler_word in self.spoiler_text:
            if re.search(r"\b" + spoiler_word + r"\b",  parse_non_spoilers(comment.body).lower()):
                return spoiler_word
        return None

    def poll(self):
        for submission in self.stream:
           if submission is None:
               return
           self.handle_submission(submission)

def create_monitor(name, config):
    logging.info("Creating Monitor for section: %s", name)
    if config["type"] == "comment":
        return CommentMonitor(name, config)
    elif config["type"] == "submission":
        return SubmissionMonitor(name, config)
    elif config["type"] == "spoiler":
        return SpoilerMonitor(name, config)
    else:
        raise ValueError("Bad config type")

def main():
    logging.basicConfig(level=logging.INFO)

    config_file = os.environ["REDDITMONITOR_CONFIG"]
    config = configparser.ConfigParser()
    config.read(config_file)
    monitors = []
    for section in config.sections():
        monitors.append(create_monitor(section, config[section]))


    while True:
        logging.info("Running Main Loop")
        for monitor in monitors:
            monitor.poll()

        time.sleep(10)

