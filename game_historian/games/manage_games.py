import sys
sys.path.append("..")

from game_historian.database.communicate_with_database import *
from game_historian.games.scrape_game_info import get_game_information


async def manage_ongoing_games(r, config_data, fbs_games, fcs_games, season):
    """
    Gathers all ongoing games and adds or updates them in the db.

    :param r: The reddit instance
    :param config_data: The config data
    :param fbs_games: The list of FBS games
    :param fcs_games: The list of FCS games
    :param season: The current season
    """

    # Loop through all FBS games and add/update them in the table
    if fbs_games is not None:
        for game in fbs_games:
            if game is not None:
                # Get information about the game
                game_info = get_game_information(r, season, "FBS", game)
                if game_info:
                    # Check if the game already exists in the table
                    if not await check_if_exists_in_table(config_data, "ongoing_games", "game_id", game_info["game_id"]):
                        if game_info["game_id"] is None:
                            print("Game ID is none for FBS game between " + game_info["home_team"] + " and " +
                                  game_info["away_team"])
                        else:
                            # Add the game to the table
                            result = await add_to_table(config_data, "ongoing_games", "game_id", game_info)
                            if result:
                                print("Added FBS game " + game_info["game_id"] + " to the table between " +
                                      game_info["home_team"] + " and " + game_info["away_team"])
                    elif game_info["is_final"] == 1:
                        # If the game is final, remove it from the table and add it to games table
                        result = await remove_from_table(config_data, "ongoing_games", "game_id", game_info["game_id"])
                        if result:
                            print("Removed FBS game " + game_info["game_id"] + " from the table between " +
                                  game_info["home_team"] + " and " + game_info["away_team"])

                        result = await add_to_table(config_data, "games", "game_id", game_info)
                        if result:
                            print("Added FBS game " + game_info["game_id"] + " between " +
                                  game_info["home_team"] + " and " + game_info["away_team"] + " to the games table")
                    else:
                        # If the game already exists, update its information
                        result = await update_table(config_data, "ongoing_games", "game_id", game_info)
                        if result:
                            print("Updated FBS game " + game_info["game_id"] + " in the table between " +
                                  game_info["home_team"] + " and " + game_info["away_team"])

    # Loop through all FCS games and add/update them in the table
    if fcs_games is not None:
        for game in fcs_games:
            if game is not None:
                # Get information about the game
                game_info = get_game_information(r, season, "FCS", game)
                if game_info:
                    # Check if the game already exists in the table
                    if not await check_if_exists_in_table(config_data, "ongoing_games", "game_id", game_info["game_id"]):
                        if game_info["game_id"] is None:
                            # If the game ID is None, print an error message
                            print("Game ID is none for FCS game between " + game_info["home_team"] + " and " +
                                  game_info["away_team"])
                        else:
                            # Add the game to the table
                            result = await add_to_table(config_data, "ongoing_games", "game_id", game_info)
                            if result:
                                print("Added FCS game " + game_info["game_id"] + " to the table between " +
                                      game_info["home_team"] + " and " + game_info["away_team"])
                    elif game_info["is_final"] == 1:
                        # If the game is final, remove it from the table and add it to games table
                        result = await remove_from_table(config_data, "ongoing_games", "game_id", game_info["game_id"])
                        if result:
                            print("Removed FCS game " + game_info["game_id"] + " from the table between " +
                                  game_info["home_team"] + " and " + game_info["away_team"])

                        result = await add_to_table(config_data, "games", "game_id", game_info)
                        if result:
                            print("Added FCS game " + game_info["game_id"] + " between " +
                                  game_info["home_team"] + " and " + game_info["away_team"] + " to the games table")
                    else:
                        # If the game already exists, update its information
                        result = await update_table(config_data, "ongoing_games", "game_id", game_info)
                        if result:
                            print("Updated FCS game " + game_info["game_id"] + " in the table between " +
                                  game_info["home_team"] + " and " + game_info["away_team"])
    else:
        print("No new games to add or update in the table")
        return False
    return True

