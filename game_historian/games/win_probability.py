import math
import pathlib
import xgboost as xgb
import pandas as pd
import sys
sys.path.append("..")

from game_historian.database.communicate_with_database import retrieve_row_from_table, retrieve_value_from_table

data = {
    'down': [4],
    'distance': [4],
    'position': [38],
    'margin': [17],
    'seconds_left_game': [350],
    'seconds_left_half': [350],
    'half': [2],
    'had_first_possession': [1],
    'elo_diff_time': [27.0449]
}


def get_win_probability(down, distance, position, margin, seconds_left_game, seconds_left_half, half,
                        had_first_possession, elo_diff_time, play_type):
    """
    Get the win probability for the play

    :param down:
    :param distance:
    :param position:
    :param margin:
    :param seconds_left_game:
    :param seconds_left_half:
    :param half:
    :param had_first_possession:
    :param elo_diff_time:
    :param play_type:
    :return:
    """

    if seconds_left_game == 0 and play_type != "PAT":
        return 1 if margin > 0 else (0 if margin < 0 else 0.5)

    if play_type == "PAT":
        prob_if_success = get_win_probability(1, 10, 75, -(margin + 1), seconds_left_game, seconds_left_half, half,
                                              1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_fail = get_win_probability(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                           1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_return = get_win_probability(1, 10, 75, -(margin - 2), seconds_left_game, seconds_left_half, half,
                                             1-had_first_possession, -elo_diff_time, 'RUN')
        return 1 - (((721 / 751) * prob_if_success) + ((27 / 751) * prob_if_fail) + ((3 / 751) * prob_if_return))
    if play_type == 'TWO_POINT':
        prob_if_success = get_win_probability(1, 10, 75, -(margin + 2), seconds_left_game, seconds_left_half, half,
                                              1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_fail = get_win_probability(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                           1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_return = get_win_probability(1, 10, 75, -(margin - 2), seconds_left_game, seconds_left_half, half,
                                             1-had_first_possession, -elo_diff_time, 'RUN')
        return 1 - (((301 / 751) * prob_if_success) + ((447  / 751) * prob_if_fail) + ((3 / 751) * prob_if_return))
    if play_type == 'KICKOFF_NORMAL':
        return 1 - get_win_probability(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                       1-had_first_possession, -elo_diff_time, 'RUN')
    if play_type == 'KICKOFF_SQUIB':
        slh = max(seconds_left_half - 5, 0)
        slg = ((2 - half) * 840) + slh
        return 1 - get_win_probability(1, 10, 65, -margin, slg, slh, half, 1-had_first_possession, -elo_diff_time,
                                       'RUN')
    if play_type == 'KICKOFF_ONSIDE':
        slh = max(seconds_left_half - 3, 0)
        slg = ((2 - half) * 840) + slh
        prob_if_success = get_win_probability(1, 10, 55, margin, slg, slh, half, 1-had_first_possession, elo_diff_time,
                                              'RUN')
        prob_if_fail = 1-get_win_probability(1, 10, 45, -margin, slg, slh, half, 1-had_first_possession, -elo_diff_time,
                                             'RUN')
        slhr = max(seconds_left_half - 10, 0)
        slgr = ((2 - half) * 840) + slh
        prob_if_return = 1-get_win_probability(1, 10, 75, margin - 6, slgr, slhr, half, 1-had_first_possession,
                                               -elo_diff_time, 'PAT')
        return ((140 / 751) * prob_if_success) + ((611 / 751) * prob_if_fail) + ((1 / 751) * prob_if_return)

    data["had_first_possession"] = [had_first_possession]
    data["margin"] = [margin]
    data["down"] = [down]
    data["distance"] = [distance]
    data["position"] = [position]
    data["seconds_left_game"] = [seconds_left_game]
    data["seconds_left_half"] = [seconds_left_half]
    data["half"] = [half]
    data["elo_diff_time"] = [elo_diff_time]

    return calculate_win_probability(data)


async def get_current_win_probability(config_data, possession, home_team, away_team, home_score, away_score, quarter,
                                      clock, ball_location, down, yards_to_go, actual_result, had_first_possession,
                                      logger):
    """
    Get the current win probability for the play

    :param config_data:
    :param possession:
    :param home_team:
    :param away_team:
    :param home_score:
    :param away_score:
    :param quarter:
    :param clock:
    :param ball_location:
    :param down:
    :param yards_to_go:
    :param actual_result:
    :param had_first_possession:
    :param logger:
    :return:
    """

    play_type = str(actual_result)
    if possession == "home":
        offense_score = home_score
        defense_score = away_score
    elif possession == "away":
        offense_score = away_score
        defense_score = home_score
    elif possession == "home" and play_type == "TOUCHDOWN":
        offense_score = str(int(home_score) + 6)
        defense_score = away_score
    elif possession == "away" and play_type == "TOUCHDOWN":
        offense_score = str(int(away_score) + 6)
        defense_score = home_score
    elif possession == "home" and play_type == "TURNOVER_TOUCHDOWN":
        offense_score = str(int(away_score) + 6)
        defense_score = home_score
    elif possession == "away" and play_type == "TURNOVER_TOUCHDOWN":
        offense_score = str(int(home_score) + 6)
        defense_score = away_score
    elif possession == "home" and play_type == "PAT":
        offense_score = str(int(home_score) + 1)
        defense_score = away_score
    elif possession == "away" and play_type == "PAT":
        offense_score = str(int(away_score) + 1)
        defense_score = home_score
    elif possession == "home" and play_type == "TWO_POINT":
        offense_score = str(int(home_score) + 2)
        defense_score = away_score
    elif possession == "away" and play_type == "TWO_POINT":
        offense_score = str(int(away_score) + 2)
        defense_score = home_score
    else:
        return
    margin = int(offense_score) - int(defense_score)

    # get seconds left in half and seconds left in game and current half
    if quarter == "1":
        seconds_left_game = 1680-(420-int(clock))
        seconds_left_half = 840-(420-int(clock))
        half = 1
    elif quarter == "2":
        seconds_left_game = 1260-(420-int(clock))
        seconds_left_half = 420-(420-int(clock))
        half = 1
    elif quarter == "3":
        seconds_left_game = 840-(420-int(clock))
        seconds_left_half = 840-(420-int(clock))
        half = 2
    elif quarter == "4":
        seconds_left_game = 420-(420-int(clock))
        seconds_left_half = 420-(420-int(clock))
        half = 2
    else:
        seconds_left_game = 0
        seconds_left_half = 0
        half = 2

    position = 100-int(ball_location)
    down = int(down)
    distance = int(yards_to_go)

    home_elo = await retrieve_value_from_table(config_data, "elo", "team", home_team, "ELO", logger)
    away_elo = await retrieve_value_from_table(config_data, "elo", "team", away_team, "ELO", logger)

    if home_elo is None:
        home_elo = 1500
    elif away_elo is None:
        away_elo = 1500

    # get elo
    if possession == "home":
        offense_elo = home_elo
        defense_elo = away_elo
    else:
        offense_elo = away_elo
        defense_elo = home_elo

    elo_diff_time = (float(offense_elo) - float(defense_elo)) * math.exp(-2 * (1 - (seconds_left_game / 1680)))

    get_win_probability(down, distance, position, margin, seconds_left_game, seconds_left_half, half, had_first_possession,
                        elo_diff_time, play_type)

    return calculate_win_probability(data)


def calculate_win_probability(win_probability_data):
    """
    Using the model, calculate the current win probability
    :param win_probability_data:
    :return:
    """

    xgb.set_config(verbosity=0)
    model_xgb = xgb.XGBRegressor(silent=True, verbosity=0)

    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())

    model_xgb.load_model(proj_dir + '/configuration/wpmodel.json')

    df_data = pd.DataFrame.from_dict(win_probability_data)
    win_probability = model_xgb.predict(df_data)

    return float(win_probability)*100
