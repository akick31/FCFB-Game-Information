import json
import pathlib

from fcfb.database.communicate_with_database import retrieve_value_from_table


def convert_to_rgb(hex):
    """
    Convert hex to RGBA

    :param hex: The hex value to convert
    :return: The RGBA value
    """

    rgb = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
    rgb_str = ''
    for value in rgb:
        rgb_str = str(value) + ", " + rgb_str
    return rgb_str


async def get_colors(config_data, home_team, away_team, logger):
    """
    Make the colors visually different, compare the two primary colors via their hex code

    :param config_data:
    :param home_team:
    :param away_team:
    :param logger:
    :return:
    """

    home_color = await retrieve_value_from_table(config_data, "teams", "name", home_team, "primary_color", logger)
    away_color = await retrieve_value_from_table(config_data, "teams", "name", away_team, "primary_color", logger)

    if home_color is None or away_color is None:
        return {'home_color': "#000000", 'away_color': "#FF0000"}

    color_comparison = compare_color(home_color, away_color)

    # Try to get secondary colors
    if not color_comparison:
        home_color = await retrieve_value_from_table(config_data, "teams", "name", home_team, "secondary_color", logger)
        away_color = await retrieve_value_from_table(config_data, "teams", "name", away_team, "secondary_color", logger)
        color_comparison = compare_color(home_color, away_color)
        if not color_comparison:
            home_color = await retrieve_value_from_table(config_data, "teams", "name", home_team, "primary_color", logger)
            away_color = await retrieve_value_from_table(config_data, "teams", "name", away_team, "secondary_color", logger)
            color_comparison = compare_color(home_color, away_color)
            if not color_comparison:
                home_color = await retrieve_value_from_table(config_data, "teams", "name", home_team, "secondary_color", logger)
                away_color = await retrieve_value_from_table(config_data, "teams", "name", away_team, "primary_color", logger)
                color_comparison = compare_color(home_color, away_color)
                if not color_comparison:
                    color_comparison = {'home_color': "#000000", 'away_color': "#FF0000"}

    return {'home_color': color_comparison['home_color'], 'away_color': color_comparison['away_color']}


def compare_color(home_color, away_color):
    """
    Compare team colors and if they're within a threshold, use black and red
    :param home_color:
    :param away_color:
    :return:
    """

    if home_color != "#000000" and home_color is not None:
        home_hex = home_color.split("#")[1]
    else:
        home_hex = "000000"
    if away_color != "#000000" and away_color is not None:
        away_hex = away_color.split("#")[1]
    else:
        away_hex = "000000"

    home_decimal = int(home_hex, 16)
    away_decimal = int(away_hex, 16)

    # If difference is greater than 330000 they are far enough apart
    if abs(home_decimal - away_decimal) > 330000:
        return {'home_color': home_color, 'away_color': away_color}
    else:
        return False


def shorten_team_name(team):
    """
    Shorten the team name so it fits on the scorebug
    :param team:
    :return:
    """

    proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
    with open(proj_dir + "/configuration/shortened_names.json", 'r') as config_file:
        shortened_names_data = json.load(config_file)

    team = team.upper()
    if "STATE" in team:
        team = team.replace('STATE', 'ST')
    if team in shortened_names_data:
        team = shortened_names_data[team]

    return team