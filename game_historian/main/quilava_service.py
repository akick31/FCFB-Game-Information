"""
Maintain the games table
"""

import sys
sys.path.append("..")

from game_historian.games.handle_ongoing_games import gather_ongoing_games
from game_historian.reddit.reddit_administration import login_reddit

if __name__ == '__main__':
    r = login_reddit()