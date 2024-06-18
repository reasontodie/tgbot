import sqlite3 as sl
from datetime import datetime as dt


class Database:
    def __init__(self):
        self.db = sl.connect('source/bot.db')
        exists = self.table_exists()
        if not exists:
            self.create_table()

    def table_exists(self) -> bool:
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE name='Vacancies';
        """)
        return cursor.fetchone() is not None

    def create_table(self) -> None:
        cursor = self.db.cursor()
        cursor.execute("""
        CREATE TABLE Vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            count INTEGER,
            datetime INTEGER
        );
        """)
        self.db.commit()

    def insert_data_to_db(self, count: int, datetime: dt) -> None:
        cursor = self.db.cursor()
        unix_timestamp = self.datetime_to_unix(datetime)
        cursor.execute("""
               INSERT INTO Vacancies (count, datetime) VALUES (?, ?)
           """, (count, unix_timestamp))
        self.db.commit()

    def get_data_from_db(self) -> list:
        cursor = self.db.cursor()
        res = cursor.execute('SELECT * FROM Vacancies')
        result = res.fetchall()
        formatted_list = [list(row) for row in result]
        for item in formatted_list:
            item[2] = self.unix_to_datetime(item[2])
        return formatted_list

    @staticmethod
    def datetime_to_unix(datetime: dt) -> int:
        return int(datetime.timestamp())

    @staticmethod
    def unix_to_datetime(unix_timestamp: int) -> dt:
        return dt.fromtimestamp(unix_timestamp)

