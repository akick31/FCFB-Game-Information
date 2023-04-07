"""
Maintain the ongoing games table
"""
import json
import asyncio
import pathlib

from reddit.reddit_administration import login_reddit


async def game_historian(r):
    """
    Run Cyndaquil service. Maintain the ongoing games table

    :param r:
    :return:
    """

    while True:
        from games.manage_games import add_ongoing_games, update_ongoing_games

        task1 = asyncio.create_task(add_ongoing_games(r, config_data))
        task2 = asyncio.create_task(update_ongoing_games(r, config_data))
        await asyncio.wait([task1, task2], return_when=asyncio.FIRST_EXCEPTION)


if __name__ == '__main__':
    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + '/game_historian/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    asyncio.run(game_historian(r))
