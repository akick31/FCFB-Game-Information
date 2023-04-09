"""
Maintain the ongoing games table
"""
import json
import asyncio
import pathlib
import logging
from os import remove
from os.path import exists

import sys
sys.path.append("..")

from game_historian.reddit.reddit_administration import login_reddit
from game_historian.games.manage_games import update_ongoing_games


async def cyndaquil_update(r, logger):
    """
    Run Cyndaquil service. Maintain the ongoing games table

    :param r:
    :param logger:
    :return:
    """

    while True:
        await update_ongoing_games(r, config_data, logger)


if __name__ == '__main__':
    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger("cyndaquil_add_logger")

    # Add Handlers
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    stream_handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

    asyncio.run(cyndaquil_update(r, logger))
