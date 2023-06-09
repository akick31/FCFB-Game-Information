import sys
sys.path.append("..")

from fcfb.database.communicate_with_database import retrieve_current_season_from_table, get_all_rows_in_table
from fcfb.games.scrape_game_plays import add_game_plays


async def add_ongoing_game_plays(r, config_data, logger):
    """
    Add all ongoing game plays to the database

    :param r:
    :param config_data:
    :param logger:
    :return:
    """

    season = await retrieve_current_season_from_table(config_data, logger)
    if season is False or season is None:
        logger.info("Failed to retrieve current season from table")
        return

    games_in_table = await get_all_rows_in_table(config_data, "ongoing_games", logger)
    if games_in_table and games_in_table is not None:
        for game in games_in_table:
            game_id = game[0]
            winning_team = game[1]
            losing_team = game[2]
            subdivision = game[27]
            if game is not None:
                await add_game_plays(r, config_data, season, subdivision, game, "plays", logger)
                logger.info("Updated " + subdivision + " game " + game_id +
                            " in the table between " + winning_team + " and "
                            + losing_team)
