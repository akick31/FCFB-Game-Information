"""
Maintain the ongoing games table
"""
import json
import asyncio
import pathlib
import sys
sys.path.append("..")

from game_historian.games.manage_games import add_ongoing_games, update_ongoing_games
from game_historian.reddit.reddit_administration import login_reddit


async def cyndaquil_service(r):
    """
    Run Cyndaquil service. Maintain the ongoing games table

    :param r:
    :return:
    """

    while True:
        tasks = [add_ongoing_games(r, config_data),
                 update_ongoing_games(r, config_data)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    config_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(config_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    asyncio.run(cyndaquil_service(r))
