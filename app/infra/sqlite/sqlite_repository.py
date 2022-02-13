import sqlite3
from contextlib import contextmanager
from sqlite3 import Cursor
from typing import Generator, List, Optional

from app.core.user.user import BitcoinWallet, User, Transaction
from app.infra.fastapi.responses import (
    CreateWalletResponse,
    GetWalletResponse,
    Response,
)


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

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS transactions(
                transaction_id INTEGER PRIMARY KEY,
                wallet_address_from TEXT NOT NULL,
                wallet_address_to TEXT NOT NULL,
                amount FLOAT NOT NULL,
                user_id_from INTEGER NOT NULL,
                user_id_to INTEGER NOT NULL,
                FOREIGN KEY(user_id_from) REFERENCES users(user_id),
                FOREIGN KEY(user_id_to) REFERENCES users(user_id)
                );"""
            )

    def get_user_id_by_api_key(self, api_key: str) -> Optional[int]:
        with self.open_db() as cursor:
            command = """SELECT user_id FROM users WHERE api_key = ?;"""
            args = (api_key,)
            cursor.execute(command, args)
            user_id = cursor.fetchone()
        if user_id is None:
            return None
        return int(user_id[0])

    def create_wallet(
            self, address: str, starting_deposit: float, api_key: str
    ) -> CreateWalletResponse:
        user_id = self.get_user_id_by_api_key(api_key)

        if user_id is None:
            return CreateWalletResponse(1, "Invalid api_key", None)

        with self.open_db() as cursor:
            command = (
                """INSERT INTO wallets(address, balance, user_id) VALUES(?,?,?);"""
            )
            args = (address, starting_deposit, int(user_id))
            cursor.execute(command, args)
            last_row_id = cursor.lastrowid
            command = """SELECT * FROM wallets where rowid = (?);"""
            args2 = (last_row_id,)
            cursor.execute(command, args2)
            row = cursor.fetchone()

        if not row:
            return CreateWalletResponse(0, "Couldn't create wallet", None)
        return CreateWalletResponse(200, "OK", BitcoinWallet(row[1], row[2], row[3]))

    def num_wallets_by_user_id(self, user_id: int) -> int:
        with self.open_db() as cursor:
            command = """SELECT * FROM wallets WHERE user_id = ?;"""
            args = (user_id,)
            cursor.execute(command, args)
            rows = cursor.fetchall()
        return len(rows)

    def get_wallets_by_user_id(self, user_id: int) -> List[BitcoinWallet]:
        wallets = []
        with self.open_db() as cursor:
            command = """SELECT * FROM wallets WHERE user_id = ?;"""
            args = (user_id,)
            cursor.execute(command, args)
            rows = cursor.fetchall()

        for row in rows:
            wallets.append(BitcoinWallet(row[1], row[2], row[3]))

        return wallets

    def get_wallet_by_address(self, address: str) -> GetWalletResponse:
        with self.open_db() as cursor:
            command = """SELECT * FROM wallets WHERE address = ?;"""
            args = (address,)
            cursor.execute(command, args)
            row = cursor.fetchone()

        if row is None:
            return GetWalletResponse(1, "Invalid address", None)

        return GetWalletResponse(200, "OK", BitcoinWallet(row[1], row[2], row[3]))

    def update_wallet_balance(self, address: str, amount: float) -> Response:
        with self.open_db() as cursor:
            command = """UPDATE wallets SET balance = balance + ? WHERE address = ?;"""
            args = (amount, address)
            cursor.execute(command, args)

        return Response(200, "OK")

    def register_transaction(
            self,
            address_from: str,
            address_to: str,
            amount: float,
            user_id_from: int,
            user_id_to: int,
    ) -> Response:
        with self.open_db() as cursor:
            command = """INSERT INTO
                transactions(wallet_address_from, wallet_address_to, amount, user_id_from, user_id_to)
                VALUES(?,?,?,?, ?);"""
            args = (address_from, address_to, amount, user_id_from, user_id_to)
            cursor.execute(command, args)

            return Response(200, "OK")

    def get_user_id_by_wallet_address(self, address: str) -> Optional[int]:
        with self.open_db() as cursor:
            command = """SELECT user_id FROM wallets WHERE address = ?;"""
            args = (address,)
            cursor.execute(command, args)
            user_row = cursor.fetchone()
        if user_row is None:
            return None
        return int(user_row[0])

    def get_wallet_transactions_by_address(self, address: str) -> List[Transaction]:
        transactions: List[Transaction] = []
        with self.open_db() as cursor:
            command = """SELECT * FROM transactions WHERE wallet_address_from = ? OR wallet_address_to = ?;"""
            args = (address, address)
            cursor.execute(command, args)
            rows = cursor.fetchall()
        for row in rows:
            transactions.append(Transaction(row[4], row[5], row[1], row[2], row[3]))
        return transactions

    def get_number_of_transactions(self) -> int:
        with self.open_db() as cursor:
            command = """SELECT COUNT(*) FROM transactions"""
            cursor.execute(command)
            return cursor.fetchone()[0]

    def get_foreign_transactions_amount(self) -> float:
        with self.open_db() as cursor:
            command = """SELECT amount FROM transactions WHERE user_id_from != user_id_to"""
            cursor.execute(command)
            rows = cursor.fetchall()
        amount: float = 0
        for row in rows:
            amount += row[0]
        return amount
