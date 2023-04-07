"""
Maintain the ongoing games table
"""
import json
import os
import asyncio
import pathlib
import sys
sys.path.append("..")

from game_historian.database.communicate_with_database import retrieve_current_season_from_table, get_num_rows_in_table, \
    get_all_rows_in_table
from game_historian.games.manage_games import add_ongoing_games, update_ongoing_games
from game_historian.reddit.reddit_administration import login_reddit

if __name__ == '__main__':
    config_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(config_dir + '/configuration/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = login_reddit(config_data)

    games_wiki = r.subreddit(config_data["subreddit"]).wiki['games']

    while True:
        fbs_games = None
        fcs_games = None

        # Gather games from wiki
        if "**FCS**" not in games_wiki.content_md and "**FBS**" not in games_wiki.content_md:
            continue
        elif "**FCS**" in games_wiki.content_md and "**FBS**" in games_wiki.content_md:
            fbs_games = games_wiki.content_md.split("**FCS**")[0].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1] \
                .split("\n")
            fcs_games = games_wiki.content_md.split("**FCS**")[1].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1] \
                .split("\n")
        elif "**FCS**" not in games_wiki.content_md and "**FBS**" in games_wiki.content_md:
            fbs_games = games_wiki.content_md.split("**FBS**")[1].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1] \
                .split("\n")

        # Remove non games from list
        for game in fbs_games:
            if "[" not in game:
                fbs_games.remove(game)
        for game in fcs_games:
            if "[" not in game:
                fcs_games.remove(game)

        # Get current season
        season = asyncio.run(retrieve_current_season_from_table(config_data))
        if season is False or (fbs_games is None and fcs_games is None):
            continue

        # Get number of games in table and verify you need to add more
        num_games_in_table = asyncio.run(get_num_rows_in_table(config_data, "ongoing_games"))
        if num_games_in_table != (len(fbs_games) + len(fcs_games)):
            asyncio.run(add_ongoing_games(r, config_data, fbs_games, fcs_games, season))

        # Get all games in table and update them
        games_in_table = asyncio.run(get_all_rows_in_table(config_data, "ongoing_games"))
        if games_in_table and games_in_table is not None:
            asyncio.run(update_ongoing_games(r, config_data, games_in_table, season))

