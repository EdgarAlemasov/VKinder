from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from settings import user_login, user_password, host, port, supreme_database_name, database_name


def create_db():
    # create our database
    connection = psycopg2.connect(user=user_login, password=user_password, host=host, port=port,
                                  database=supreme_database_name)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = f'create database {database_name}'
    cursor.execute(sql_create_database)
    # connect to our database
    engine = create_engine(f'postgresql+psycopg2://{user_login}:{user_password}@localhost:{host}/{database_name}')
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
        engine = create_engine(f'postgresql+psycopg2://{user_login}:{user_password}@localhost:{host}/{database_name}')
        connection = engine.connect()
        connection.execute(f"""
            INSERT INTO users (user_id, first_name, url)
            VALUES
                ('{values['user_id']}', '{values['name']}', '{values['user_link']}')
        """)


def delete_db():
    connection = psycopg2.connect(user=user_login, password=user_password, host=host, port=port,
                                  database=supreme_database_name)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = f'DROP DATABASE {database_name}'
    cursor.execute(sql_create_database)
