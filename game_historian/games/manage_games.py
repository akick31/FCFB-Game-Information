import concurrent.futures
import sys
import asyncio
sys.path.append("..")

from game_historian.database.communicate_with_database import *
from game_historian.games.scrape_game_info import get_game_information


# Define a coroutine function to get game information
async def get_game_info(r, season, subdivison, game, from_wiki):
    """
    Gets the game information for a game asynchronously.

    :param r:
    :param season:
    :param subdivison:
    :param game:
    :param from_wiki:
    :return:
    """

    game_info = get_game_information(r, season, subdivison, game, from_wiki)
    return game_info


async def add_ongoing_games(r, config_data, fbs_games, fcs_games, season):
    """
    Gathers all ongoing games and adds them in the db.

    :param r: The reddit instance
    :param config_data: The config data
    :param fbs_games: The list of FBS games
    :param fcs_games: The list of FCS games
    :param season: The current season
    """

    # Retrieve all FBS and FCS games in parallel
    tasks = []
    if fbs_games is not None:
        tasks.extend([get_game_info(r, season, "FBS", game, True) for game in fbs_games if game is not None])
    if fcs_games is not None:
        tasks.extend([get_game_info(r, season, "FCS", game, True) for game in fcs_games if game is not None])
    game_information_list = await asyncio.gather(*tasks)

    # Loop through all game information and add the games in the table
    existing_game_ids = set(await get_all_values_in_column_from_table(config_data, "ongoing_games", "game_id"))
    for game_info in game_information_list:
        if game_info:
            if game_info["game_id"] not in existing_game_ids:
                if game_info["game_id"] is None:
                    print("Game ID is none for game between " + game_info["home_team"] + " and " + game_info["away_team"])
                else:
                    result = await add_to_table(config_data, "ongoing_games", "game_id", game_info)
                    if result:
                        print("Added game " + game_info["game_id"] + " to the table between " + game_info["home_team"] +
                              " and " + game_info["away_team"])
        else:
            print("Failed to get game information")

    return True


async def update_ongoing_games(r, config_data, games_in_table, season):
    """
    Gathers all ongoing games and adds them in the db.

    :param r: The reddit instance
    :param config_data: The config data
    :param games_in_table: The list of games
    :param season: The current season
    """

    # Loop through all games and update them in the table
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_game = {}
        for game in games_in_table:
            subdivision = game[27]
            if game is not None:
                future = executor.submit(get_game_information, r, season, subdivision, game, False)
                future_to_game[future] = game

        for future in concurrent.futures.as_completed(future_to_game):
            game = future_to_game[future]
            game_info = future.result()
            if game_info and game_info["game_id"] is not None:
                if game_info["is_final"] == 1:
                    # If the game is final, remove it from the table and add it to games table
                    result = await remove_from_table(config_data, "ongoing_games", "game_id", game_info["game_id"])
                    if result:
                        print("Removed " + subdivision + " game " + game_info["game_id"] +
                              " from the table between " + game_info["home_team"] + " and " + game_info["away_team"])

                    result = await add_to_table(config_data, "games", "game_id", game_info)
                    if result:
                        print("Added " + subdivision + " game " + game_info["game_id"] + " between " +
                              game_info["home_team"] + " and " + game_info["away_team"] + " to the games table")
                else:
                    # If the game already exists, update its information
                    result = await update_table(config_data, "ongoing_games", "game_id", game_info)
                    if result:
                        print("Updated " + subdivision + " game " + game_info["game_id"] +
                              " in the table between " + game_info["home_team"] + " and " + game_info["away_team"])
    return True

