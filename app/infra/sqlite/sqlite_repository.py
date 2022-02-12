import sqlite3
from contextlib import contextmanager
from sqlite3 import Cursor
from typing import Generator


class SQLiteRepository:
    def __init__(self, db_name: str = "bitcoin-wallet.db") -> None:
        self.db_name = db_name
        self.__create_tables()

    @contextmanager
    def open_db(self) -> Generator[Cursor, None, None]:
        connection = sqlite3.connect(self.db_name)
        try:
            cursor = connection.cursor()
            yield cursor
        finally:
            connection.commit()
            connection.close()

    def register_user(self, api_key_magari: str) -> None:
        with self.open_db() as cursor:
            command = """INSERT INTO users(api_key) VALUES(?);"""
            args = (api_key_magari,)
            cursor.execute(command, args)

    def __create_tables(self) -> None:
        with self.open_db() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                   api_key TEXT NOT NULL UNIQUE);"""
            )
