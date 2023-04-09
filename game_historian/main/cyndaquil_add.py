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
from game_historian.games.manage_games import add_ongoing_games


async def cyndaquil_add(r, logger):
    """
    Run Cyndaquil service. Add to the the ongoing games table

    :param r:
    :param logger:
    :return:
    """

    while True:
        await add_ongoing_games(r, config_data, logger)


if __name__ == '__main__':
    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    if exists(proj_dir + '/logs/cyndaquil_add.log'):
        remove(proj_dir + '/logs/cyndaquil_add.log')

    logging.basicConfig(filename=proj_dir + '/logs/cyndaquil_add.log',
                        format='[%(asctime)s] [%(levelname)s] - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger("cyndaquil_add_logger")

    # Add file handler
    file_handler = logging.FileHandler(proj_dir + '/logs/cyndaquil_add.log', mode='w')
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    asyncio.run(cyndaquil_add(r, logger))
