from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_db():
    # create our database
    connection = psycopg2.connect(user="postgres", password="ImAlive72ae", host="127.0.0.1", port="5432",
                                  database="postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = 'create database vkinder72'
    cursor.execute(sql_create_database)
    # connect to our database
    engine = create_engine('postgresql+psycopg2://postgres:ImAlive72ae@localhost:5432/vkinder72')
    connection = engine.connect()
    connection.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            id INT GENERATED ALWAYS AS IDENTITY,
            user_id VARCHAR(40) NOT NULL,
            first_name VARCHAR(40) NOT NULL,
            url VARCHAR(40) NOT NULL
        );
    """)


def add_info(final_dict):
    for key, values in final_dict.items():
        engine = create_engine('postgresql+psycopg2://postgres:ImAlive72ae@localhost:5432/vkinder72')
        connection = engine.connect()
        connection.execute(f"""
            INSERT INTO users (user_id, first_name, url)
            VALUES
                ('{values['user_id']}', '{values['name']}', '{values['user_link']}')
        """)


def delete_db():
    connection = psycopg2.connect(user="postgres", password="ImAlive72ae", host="127.0.0.1", port="5432",
                                  database="postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = 'DROP DATABASE vkinder72'
    cursor.execute(sql_create_database)
