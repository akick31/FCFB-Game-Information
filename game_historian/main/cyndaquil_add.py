"""
Maintain the ongoing games table
"""
import json
import asyncio
import pathlib
import sys
sys.path.append("..")

from game_historian.reddit.reddit_administration import login_reddit
from game_historian.games.manage_games import add_ongoing_games


async def cyndaquil_add(r):
    """
    Run Cyndaquil service. Add to the the ongoing games table

    :param r:
    :return:
    """

    while True:
        await add_ongoing_games(r, config_data)


if __name__ == '__main__':
    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    asyncio.run(cyndaquil_add(r))
