import sqlite3
from contextlib import contextmanager
from sqlite3 import Cursor
from typing import Generator, List

from app.core.user.user import BitcoinWallet, User


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

    def register_user(self, user: User) -> None:
        with self.open_db() as cursor:
            command = """INSERT INTO users(api_key, name) VALUES(?,?);"""
            args = (
                user.api_key,
                user.name,
            )
            cursor.execute(command, args)

    def __create_tables(self) -> None:
        with self.open_db() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                api_key TEXT UNIQUE ,
                name TEXT NOT NULL);"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS wallets (
                wallet_id INTEGER PRIMARY KEY,
                address TEXT UNIQUE ,
                balance FLOAT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
                );"""
            )

    def get_user_id_by_api_key(self, api_key: str) -> int:
        with self.open_db() as cursor:
            command = """SELECT user_id FROM users WHERE api_key = ?;"""
            args = (api_key,)
            cursor.execute(command, args)
            user_id = cursor.fetchone()
        return int(user_id[0])

    def create_wallet(
        self, address: str, starting_deposit: float, api_key: str
    ) -> BitcoinWallet:
        user_id = self.get_user_id_by_api_key(api_key)

        with self.open_db() as cursor:
            command = (
                """INSERT INTO wallets(address, balance, user_id) VALUES(?,?,?);"""
            )
            args = (address, starting_deposit, user_id)
            cursor.execute(command, args)
            last_row_id = cursor.lastrowid
            command = """SELECT * FROM wallets where rowid = ?;"""
            args = (last_row_id,)
            cursor.execute(command, args)
            row = cursor.fetchone()

        return BitcoinWallet(row[0], row[1], row[2])

    def get_wallets_by_user_id(self, user_id: int) -> List[BitcoinWallet]:
        wallets = []
        with self.open_db() as cursor:
            command = """SELECT * FROM wallets WHERE user_id = ?;"""
            args = (user_id,)
            cursor.execute(command, args)
            rows = cursor.fetchall()

        for row in rows:
            wallets.append(BitcoinWallet(row[0], row[1], row[2]))

        return wallets
