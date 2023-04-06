from game_historian.database.communicate_with_database import *
from game_historian.games.scrape_game_info import get_game_information


async def gather_ongoing_games(r, config_data):
    """
    Gathers all ongoing games and adds them to the db.
    """

    games_wiki = r.subreddit(config_data["subreddit"]).wiki['games']
    fbs_games = None
    fcs_games = None

    if "**FCS**" not in games_wiki.content_md and "**FBS**" not in games_wiki.content_md:
        return False
    elif "**FCS**" in games_wiki.content_md and "**FBS**" in games_wiki.content_md:
        fbs_games = games_wiki.content_md.split("**FCS**")[0].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1]\
            .split("\n")
        fcs_games = games_wiki.content_md.split("**FCS**")[1].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1]\
            .split("\n")
    elif "**FCS**" not in games_wiki.content_md and "**FBS**" in games_wiki.content_md:
        fbs_games = games_wiki.content_md.split("**FBS**")[1].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1]\
            .split("\n")

    # Remove non games from list
    for game in fbs_games:
        if "[" not in game:
            fbs_games.remove(game)
    for game in fcs_games:
        if "[" not in game:
            fcs_games.remove(game)

    season = await retrieve_current_season_from_table(config_data)

    if season is not False:
        if fbs_games is not None:
            for game in fbs_games:
                if game is not None:
                    game_info = get_game_information(r, season, "FBS", game)
                    if game_info is not False and not await check_if_exists_in_table(config_data, "ongoing_games",
                                                                                     "game_id", game_info["game_id"]):
                        result = await add_values_to_table(config_data, "ongoing_games", "game_id", game_info)
                        if result:
                            print("Added FBS game " + game_info["game_id"] + " to the table between " + game_info["home_team"] +
                                  " and " + game_info["away_team"])
        if fcs_games is not None:
            for game in fcs_games:
                if game is not None:
                    game_info = get_game_information(r, season, "FBS", game)
                    if game_info is not False and not await check_if_exists_in_table(config_data, "ongoing_games",
                                                                                     "game_id", game_info["game_id"]):
                        result = await add_values_to_table(config_data, "ongoing_games", "game_id", game_info)
                        if result:
                            print("Added FCS game " + game_info["game_id"] + " to the table between " + game_info["home_team"] +
                                  " and " + game_info["away_team"])
