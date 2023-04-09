import requests
import sys
sys.path.append("..")

from game_historian.database.communicate_with_database import get_num_rows_for_value_in_table, add_to_table_with_conflict
from game_historian.games.scrape_game_info import get_game_information
from game_historian.games.win_probability import get_current_win_probability


def parse_data_from_github(gist_url):
    """
    Parse the data from the Github Gist into data.txt
    :param gist_url:
    :return:
    """

    # Parse data from the github url
    url = gist_url + "/raw"
    gist = requests.get(url)

    # Remove the very first line from the data
    data = ""
    flag = 0
    for character in gist.text:
        if flag == 0 and character == "0":
            data = data + "0"
            flag = 1
        elif flag == 1:
            data = data + character
    if data.find('--------------------------------------------------------------------------------\n') >= 0:
        data = data.replace('--------------------------------------------------------------------------------\n', '-')
    if data.find('--------------------------------------------------------------------------------') >= 0:
        data = data.replace('--------------------------------------------------------------------------------', '-')

    return data


async def add_game_plays(r, config_data, season, subdivision, game, logger):
    """
    Iterate through the gist and add each line and the win probability to the database

    :param r:
    :param config_data:
    :param season:
    :param subdivision:
    :param game:
    :param logger:
    :return:
    """

    game_info = get_game_information(r, season, subdivision, game, False)
    home_team = game_info['home_team']
    away_team = game_info['away_team']
    gist_url = game_info['gist_url']

    gist_data = parse_data_from_github(gist_url)

    # split game into plays
    plays = gist_data.split("\n")
    if "--" in plays:
        plays.remove("--")
    if "-" in plays:
        plays.remove("-")

    num_plays_added = await get_num_rows_for_value_in_table(config_data, "game_plays", "game_id", game_info["game_id"],
                                                            logger)

    # If the number of plays is the same as the number of plays in the database, you already added everything to add
    if len(plays) == num_plays_added:
        return
    else:
        play_number = num_plays_added + 1

    for play_num in range(play_number, len(plays)):
        play = plays[play_num]

        first_play_possession = plays[1].split("|")[5]
        if first_play_possession == "home":
            had_first_possession = 0
        elif first_play_possession == "away":
            had_first_possession = 1
        else:
            logger.error("Could not determine who had first possession")
            return

        if "----" not in play and play != "-":
            play_information = play.split("|")
            home_score = play_information[0]
            home_score = str(abs(int(home_score)))
            away_score = play_information[1]
            away_score = str(abs(int(away_score)))
            game_quarter = play_information[2]
            clock = play_information[3]
            ball_location = play_information[4]
            possession = play_information[5]
            down = play_information[6]
            yards_to_go = play_information[7]
            defensive_number = play_information[8]
            if defensive_number == "":
                defensive_number = "0"

            offensive_number = play_information[9]
            if offensive_number == "":
                offensive_number = "0"

            defensive_submitter = play_information[10]
            offensive_submitter = play_information[11]
            play = play_information[12]
            result = play_information[13]
            actual_result = play_information[14]
            yards = play_information[15]
            if yards == "":
                yards = "0"

            play_time = play_information[16]
            if play_time == "":
                play_time = "0"

            runoff_time = play_information[17]
            if runoff_time == "":
                runoff_time = "0"

            win_probability = str(await get_current_win_probability(config_data, possession, home_team, away_team,
                                                                    home_score, away_score, game_quarter, clock,
                                                                    ball_location, down, yards_to_go, actual_result,
                                                                    had_first_possession, logger))

            play_json = {
                "game_id": game_info["game_id"],
                "home_team": home_team,
                "away_team": away_team,
                "play_number": play_number,
                "home_score": home_score,
                "away_score": away_score,
                "game_quarter": game_quarter,
                "clock": clock,
                "ball_location": ball_location,
                "possession": possession,
                "down": down,
                "yards_to_go": yards_to_go,
                "defensive_number": defensive_number,
                "offensive_number": offensive_number,
                "defensive_submitter": defensive_submitter,
                "offensive_submitter": offensive_submitter,
                "play": play,
                "result": result,
                "actual_result": actual_result,
                "yards": yards,
                "play_time": play_time,
                "runoff_time": runoff_time,
                "win_probability": win_probability
            }

            if play_number > num_plays_added:
                await add_to_table_with_conflict(config_data, "game_plays", "game_id", "play_number", play_json,
                                                 logger)
                # update_game_stats(game_id, play_information)

            play_number = play_number + 1
