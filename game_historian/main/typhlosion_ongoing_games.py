"""
Maintain the ongoing games table
"""
import json
import asyncio
import pathlib
import logging

import sys

sys.path.append("..")

from game_historian.reddit.reddit_administration import login_reddit
from game_historian.games.manage_plays import add_ongoing_game_plays


async def typhlosion_ongoing_games(r, logger):
    """
    Run Cyndaquil service. Maintain the ongoing games table

    :param r:
    :param logger:
    :return:
    """

    while True:
        await add_ongoing_game_plays(r, config_data, logger)


if __name__ == '__main__':
    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger("typhlosion_ongoing_games_logger")

    # Add Handlers
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    stream_handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

    asyncio.run(typhlosion_ongoing_games(r, logger))
