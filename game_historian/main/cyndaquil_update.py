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
    logger = logging.getLogger("cyndaquil_update_logger")

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler
    file_handler = logging.FileHandler(proj_dir + '/logs/cyndaquil_update.log', mode='a+')
    logger.addHandler(file_handler)

    asyncio.run(cyndaquil_update(r, logger))
