import praw
import json
import os


def login_reddit(config_data):
    """
    Login to reddit
    """

    r = praw.Reddit(user_agent=config_data['user_agent'],
                    client_id=config_data['client_id'],
                    client_secret=config_data['client_secret'],
                    username=config_data['username'],
                    password=config_data['password'],
                    subreddit=config_data['subreddit'],
                    check_for_async=False)
    return r
