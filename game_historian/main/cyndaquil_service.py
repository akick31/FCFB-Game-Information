"""
Maintain the ongoing games table
"""
import json
import os
import sys
import asyncio
sys.path.append("..")

from game_historian.games.handle_ongoing_games import gather_ongoing_games
from game_historian.reddit.reddit_administration import login_reddit

if __name__ == '__main__':
    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    with open(main_dir + '/game_historian/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)
    asyncio.run(gather_ongoing_games(r, config_data))
