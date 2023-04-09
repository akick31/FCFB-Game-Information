import logging
from game_historian.database.connect_to_database import connect_to_db


async def add_to_table(config_data, table_name, where_column, values_json, logger):
    """
    Add values to a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param values_json:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()

        # Insert the id of the game
        where_value = values_json[where_column]
        cursor.execute("INSERT INTO " + table_name + "(" + where_column + ") VALUES ('" + where_value + "')")
        db.commit()

        for column, value in values_json.items():
            cursor = db.cursor()
            if isinstance(value, int) or isinstance(value, float):
                cursor.execute("UPDATE " + table_name + " SET " + column + "=" + str(value) + " " +
                               "WHERE " + where_column + " = '" + str(where_value) + "'")
            else:
                cursor.execute("UPDATE " + table_name + " SET " + column + "='" + value + "'" +
                               "WHERE " + where_column + " = '" + str(where_value) + "'")
            db.commit()
    except Exception as e:
        logger.error("Error adding value to database table " + table_name + ": " + str(e))
        db.close()
        return None

    db.close()
    return True


async def add_to_table_with_conflict(config_data, table_name, where_column, conflict_column, values_json, logger):
    """
    Add values to a table with a defined conflict check between two columns

    :param config_data:
    :param table_name:
    :param where_column:
    :param conflict_column:
    :param values_json:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()

        # Insert the id of the game
        where_value = values_json[where_column]
        cursor.execute("INSERT INTO " + table_name + " (" + where_column + ", " + conflict_column + ") " +
                       "VALUES ('" + where_value + "', " + str(values_json[conflict_column]) + ")")
        db.commit()

        for column, value in values_json.items():
            cursor = db.cursor()
            if isinstance(value, int) or isinstance(value, float):
                cursor.execute("UPDATE " + table_name + " SET " + column + "=" + str(value) + " " +
                               "WHERE " + where_column + " = '" + str(where_value) + "' " +
                               "ON CONFLICT (" + where_column + ", " + conflict_column + ") DO NOTHING")
            else:
                cursor.execute("UPDATE " + table_name + " SET " + column + "='" + value + "'" +
                               "WHERE " + where_column + " = '" + str(where_value) + "' " +
                               "ON CONFLICT (" + where_column + ", " + conflict_column + ") DO NOTHING")
            db.commit()
    except Exception as e:
        logger.error("Error adding value to database table " + table_name + ": " + str(e))
        db.close()
        return None

    db.close()
    return True


async def remove_from_table(config_data, table_name, where_column, where_value, logger):
    """
    Remove a value from a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param where_value:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM " + table_name + " WHERE " + where_column + " = '" + str(where_value) + "'")
        db.commit()
    except Exception as e:
        logger.error("Error removing value from database table " + table_name + ": " + str(e))
        db.close()
        return None

    db.close()
    return True


async def update_table(config_data, table_name, where_column, values_json, logger):
    """
    Update a value in a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param values_json:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        where_value = values_json[where_column]
        for column, value in values_json.items():
            cursor = db.cursor()
            if isinstance(value, int) or isinstance(value, float):
                cursor.execute("UPDATE " + table_name + " SET " + column + "=" + str(value) + " " +
                               "WHERE " + where_column + " = '" + str(where_value) + "'")
            elif value is not None:
                cursor.execute("UPDATE " + table_name + " SET " + column + "='" + value + "'" +
                               "WHERE " + where_column + " = '" + str(where_value) + "'")
            db.commit()
    except Exception as e:
        logger.error("Error updating value in database table " + table_name + ": " + str(e))
        db.close()
        return None

    db.close()
    return True


async def retrieve_row_from_table(config_data, table_name, where_column, where_value, logger):
    """
    Update a value in a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param where_value:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name +
                       " WHERE " + where_column + "=" + where_value)
        row = cursor.fetchall()
        db.close()
        return row
    except Exception as e:
        logger.error("Error retrieving row from database table " + table_name + ": " + str(e))
        db.close()
        return None


async def retrieve_value_from_table(config_data, table_name, where_column, where_value, column, logger):
    """
    Retrieve a value from a table

    :param config_data:
    :param table_name:
    :param where_column:
    :param where_value:
    :param column:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT " + column + " FROM " + table_name +
                       " WHERE " + where_column + "='" + where_value + "'")
        value = cursor.fetchone()
        db.close()
        return value[0]
    except Exception as e:
        logger.error("Error retrieving value from database table " + table_name + ": " + str(e))
        db.close()
        return None


async def retrieve_current_season_from_table(config_data, logger):
    """
    Update a value in a table

    :param config_data:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM seasons " +
                       "ORDER BY season DESC LIMIT 1")
        season = cursor.fetchone()
        db.close()
        return season[0]
    except Exception as e:
        logger.error("Error retrieving season from seasons table: " + str(e))
        db.close()
        return None


async def check_if_exists_in_table(config_data, table_name, column_name, value, logger):
    """
    Check if a value exists in a table

    :param config_data:
    :param table_name:
    :param column_name:
    :param value:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name +
                       " WHERE " + column_name + "='" + value + "'")
        row = cursor.fetchone()
        db.close()
        if row is None:
            return False
        else:
            return True
    except Exception as e:
        logger.error("Error checking if value exists in database table " + table_name + ": " + str(e))
        db.close()
        return None


async def get_num_rows_in_table(config_data, table_name, logger):
    """
    Return the number of rows in a table

    :param config_data:
    :param table_name:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        row = cursor.fetchall()
        db.close()
        return len(row)
    except Exception as e:
        logger.error("Error retrieving number of rows in database table " + table_name + ": " + str(e))
        db.close()
        return None


async def get_all_rows_in_table(config_data, table_name, logger):
    """
    Return all rows in a table

    :param config_data:
    :param table_name:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        rows = cursor.fetchall()
        db.close()
        return rows
    except Exception as e:
        logger.error("Error retrieving all rows in database table " + table_name + ": " + str(e))
        db.close()
        return None


async def get_all_values_in_column_from_table(config_data, table_name, column_name, logger):
    """
    Return all values in a column from a table

    :param config_data:
    :param table_name:
    :param column_name:
    :param logger:
    :return:
    """

    # Connect to the database
    db = await connect_to_db(config_data)
    if db is None:
        logger.error("Error connecting to the database, please try again later")
        return False

    try:
        cursor = db.cursor()
        cursor.execute("SELECT " + column_name + " FROM " + table_name)
        values = cursor.fetchall()
        db.close()
        return [value[0] for value in values]
    except Exception as e:
        logger.error("Error retrieving all values in column " + column_name + " from database table " + table_name
                     + ": " + str(e))
        db.close()
        return None
