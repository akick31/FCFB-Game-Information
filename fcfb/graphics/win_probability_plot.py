import numpy as np
import matplotlib.pyplot as plt

from fcfb.database.communicate_with_database import get_all_rows_where_value_in_column_from_table
from fcfb.graphics.graphic_utils import *


async def plot_win_probability(config_data, game_id, logger):
    game_plays = await get_all_rows_where_value_in_column_from_table(config_data, "game_plays", "game_id", game_id, logger)
    if game_plays is None or len(game_plays) == 0:
        return

    home_team = game_plays[0][21]
    away_team = game_plays[0][22]

    color_dict = await get_colors(config_data, home_team, away_team, logger)
    home_color = color_dict["home_color"]
    away_color = color_dict["away_color"]

    play_number_arr = []
    home_win_probability_arr = []
    away_win_probability_arr = []
    for play in game_plays:
        play_number_arr.append(play[1])
        if play[7] == "home":
            cur_win_probability = play[20] * 100
            home_win_probability_arr.append(cur_win_probability)
            away_win_probability_arr.append(100 - cur_win_probability)
        else:
            cur_win_probability = play[20] * 100
            home_win_probability_arr.append(100 - cur_win_probability)
            away_win_probability_arr.append(cur_win_probability)

    play_number_arr = np.array(play_number_arr)
    home_win_probability_arr = np.array(home_win_probability_arr)
    away_win_probability_arr = np.array(away_win_probability_arr)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw=dict(wspace=0.0, hspace=0, bottom=0.5 / (2 + 1), left=0.5 / (3)))
    l1 = ax1.plot(play_number_arr, home_win_probability_arr, home_color, linewidth=1)
    l2 = ax2.plot(play_number_arr, away_win_probability_arr, away_color, linewidth=1)

    ax2.invert_yaxis()
    lim = max(max(ax1.get_ylim()), max(ax2.get_ylim()))
    ax1.set_ylim(50, lim)
    ax2.set_ylim(lim, 50)
    plt.legend(l1+l2, [home_team, away_team])

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.ylabel("Win Probability (%)")
    plt.xlabel("Play")
    top_ticks = [50, 60, 70, 80, 90, 100]
    bottom_ticks = [50, 60, 70, 80, 90, 100]
    ax1.set_yticks(top_ticks)
    ax2.set_yticks(bottom_ticks)
    ax1.set_title("Win Probability", loc="center")
    ax1.legend(l1, [home_team], loc="upper left")
    ax2.legend(l2, [away_team], loc="lower left")

    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    plot_img = proj_dir + "/graphics/win_probability/" + game_id + "_wp.png"
    plt.savefig(plot_img)
    plt.close()
    return "/home/apkick/fcfb_win_probability/" + game_id + "_wp.png"
