from game_historian.database.communicate_with_database import *
from game_historian.games.scrape_game_info import *
from datetime import datetime


async def search_for_game_thread(config_data, r, winning_team, losing_team, winning_score, losing_score, season, logger):
    """
    Searches for a game thread for a given game
    :param config_data: The configuration data
    :param r: The reddit instance
    :param winning_team: The winning team
    :param losing_team: The losing team
    :param winning_score: The winning score
    :param losing_score: The losing score
    :param season: The season
    :param logger: The logger
    :return: The game thread
    """

    for submission in r.subreddit("FakeCollegeFootball").search("[POSTGAME THREAD] " + winning_team + " defeats "
                                                                + losing_team + ", " + str(winning_score) + "-"
                                                                + str(losing_score), sort='new'):
        if submission.link_flair_text is None or "Game Thread" not in submission.link_flair_text:
            continue
        home_team = get_home_team(submission.selftext)
        away_team = get_away_team(submission.selftext)
        home_score = get_home_score(submission.selftext)
        away_score = get_away_score(submission.selftext)
        game_time = datetime.fromtimestamp(int(submission.created_utc))

        season_start = await retrieve_value_from_table(config_data, "seasons", "season", season, "season_start", logger)
        season_end = await retrieve_value_from_table(config_data, "seasons", "season", season, "season_end", logger)
        postseason_start = await retrieve_value_from_table(config_data, "seasons", "season", season, "postseason_start",
                                                           logger)

        if season_end is None or postseason_start is None:
            season_end = datetime.now()

        if not (season_start < game_time < season_end):
            if postseason_start is not None:
                if not (game_time > postseason_start):
                    continue
            else:
                continue

        if home_team.lower() == winning_team.lower() and away_team.lower() == losing_team.lower() and home_score == winning_score\
                and away_score == losing_score:
            if submission.link_flair_text != "Post Game Thread":
                return r.submission(url=submission.url)
            body = submission.selftext
            game_thread = body.split("[Game thread](")[1].split(")")[0]
            return r.submission(url=game_thread)
        elif away_team.lower() == winning_team.lower() and home_team.lower() == losing_team.lower() and away_score == winning_score\
                and home_score == losing_score:
            if submission.link_flair_text != "Post Game Thread":
                return r.submission(url=submission.url)
            body = submission.selftext
            game_thread = body.split("[Game thread](")[1].split(")")[0]
            return r.submission(url=game_thread)

    return False