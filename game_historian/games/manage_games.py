import concurrent.futures
import logging
import sys
sys.path.append("..")

from game_historian.database.communicate_with_database import *
from game_historian.games.scrape_game_info import get_game_information, get_game_id


# Define a coroutine function to get game information
async def get_game_info(config_data, r, season, subdivison, game, requester, logger):
    """
    Gets the game information for a game asynchronously.

    :param config_data:
    :param r:
    :param season:
    :param subdivison:
    :param game:
    :param requester:
    :param logger:
    :return:
    """

    game_info = await get_game_information(config_data, r, season, subdivison, game, requester, logger)
    return game_info


async def add_ongoing_games(r, config_data, logger):
    """
    Gathers all ongoing games and adds them in the db.

    :param r: The reddit instance
    :param config_data: The config data
    :param logger: The logger
    """

    games_wiki = r.subreddit(config_data["subreddit"]).wiki['games']

    fbs_games = None
    fcs_games = None

    # Gather games from wiki
    if "**FCS**" not in games_wiki.content_md and "**FBS**" not in games_wiki.content_md:
        return
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

    if fbs_games is None and fcs_games is None:
        logger.info("No games in the wiki to add to table")
        return

    # Get current season
    season = await retrieve_current_season_from_table(config_data, logger)
    if season is False or season is None:
        logger.error("Failed to retrieve current season from table")
        return

    # Get number of games in table and verify you need to add more
    num_games_in_table = await get_num_rows_in_table(config_data, "ongoing_games", logger)
    if num_games_in_table != (len(fbs_games) + len(fcs_games) - 1):
        for game in fbs_games:
            if game is not None and "link" in game:
                game_link = game.split(")|[rerun]")[0].split("[link](")[1]
                game_link_id = game_link.split("/comments")[1]

                submission = r.submission(game_link_id)
                submission_body = submission.selftext

                game_id = get_game_id(submission_body)

                # Loop through all game information and add the games in the table
                existing_game_ids = set(await get_all_values_in_column_from_table(config_data, "ongoing_games",
                                                                                  "game_id", logger))
                if game_id not in existing_game_ids:
                    game_info = await get_game_info(config_data, r, season, "FBS", game, "wiki", logger)
                    if game_info:
                        if game_info["game_id"] is None:
                            logger.info("Game ID is none for the FBS game between " + game_info["home_team"] + " and "
                                        + game_info["away_team"])
                        else:
                            result = await add_to_table(config_data, "ongoing_games", "game_id", game_info, logger)
                            if result:
                                logger.info("Added FBS game " + game_info["game_id"] + " to the table between "
                                            + game_info["home_team"] + " and " + game_info["away_team"])
                            else:
                                logger.error("Failed to get FBS game information")
                else:
                    logger.info("FBS game " + game_id + " already exists in the table")
        for game in fcs_games:
            if game is not None:
                game_link = game.split(")|[rerun]")[0].split("[link](")[1]
                game_link_id = game_link.split("/comments")[1]

                submission = r.submission(game_link_id)
                submission_body = submission.selftext

                game_id = get_game_id(submission_body)

                # Loop through all game information and add the games in the table
                existing_game_ids = set(await get_all_values_in_column_from_table(config_data, "ongoing_games",
                                                                                  "game_id", logger))
                if game_id not in existing_game_ids:
                    game_info = await get_game_info(config_data, r, season, "FCS", game, "wiki", logger)
                    if game_info:
                        if game_info["game_id"] is None:
                            logger.info("Game ID is none for the FCS game between " + game_info["home_team"] + " and "
                                        + game_info["away_team"])
                        else:
                            result = await add_to_table(config_data, "ongoing_games", "game_id", game_info, logger)
                            if result:
                                logger.info("Added FCS game " + game_info["game_id"] + " to the table between "
                                            + game_info["home_team"] + " and " + game_info["away_team"])
                            else:
                                logger.error("Failed to get FCS game information")
                else:
                    logger.info("FCS game " + game_id + " already exists in the table")

        return True
    else:
        logger.info("No new games to add to table, number of games in table matches number of games in wiki")
        return False


async def update_ongoing_games(r, config_data, logger):
    """
    Gathers all ongoing games and adds them in the db.

    :param r: The reddit instance
    :param config_data: The config data
    :param logger: The logger
    """

    season = await retrieve_current_season_from_table(config_data, logger)
    if season is False or season is None:
        logger.info("Failed to retrieve current season from table")
        return

    games_in_table = await get_all_rows_in_table(config_data, "ongoing_games", logger)
    if games_in_table and games_in_table is not None:
        # Loop through all games and update them in the table
        for game in games_in_table:
            subdivision = game[27]
            if game is not None:
                game_info = await get_game_information(config_data, r, season, subdivision, game, "update", logger)
                if game_info and game_info["game_id"] is not None:
                    if game_info["is_final"] == 1:
                        # If the game is final, remove it from the table and add it to games table
                        result = await remove_from_table(config_data, "ongoing_games", "game_id", game_info["game_id"],
                                                         logger)
                        if result:
                            logger.info("Removed " + subdivision + " game " + game_info["game_id"] +
                                        " from the table between " + game_info["home_team"] + " and "
                                        + game_info["away_team"])

                        result = await add_to_table(config_data, "games", "game_id", game_info, logger)
                        if result:
                            logger.info("Added " + subdivision + " game " + game_info["game_id"] + " between " +
                                        game_info["home_team"] + " and " + game_info["away_team"]
                                        + " to the games table")
                    else:
                        # If the game already exists, update its information
                        result = await update_table(config_data, "ongoing_games", "game_id", game_info, logger)
                        if result:
                            logger.info("Updated " + subdivision + " game " + game_info["game_id"] +
                                        " in the table between " + game_info["home_team"] + " and "
                                        + game_info["away_team"])
        return True
