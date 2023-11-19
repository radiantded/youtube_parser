import psycopg2

from config import (
    DB_HOST, DB_PORT, POSTGRES_DB,
    POSTGRES_PASSWORD, POSTGRES_USER
)
from data_classes import Video


class Database:
    def __enter__(self):
        self.conn = psycopg2.connect(
            f'host={DB_HOST} port={DB_PORT} dbname={POSTGRES_DB}\
              user={POSTGRES_USER} password={POSTGRES_PASSWORD}'
        )
        self.cursor = self.conn.cursor()
        self.create_table()
        return self

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            videos(
                channel_username CHAR(50) NOT NULL,
                video_id CHAR(50) NOT NULL UNIQUE,
                video_href CHAR(100) NOT NULL
            );
        """)
        self.conn.commit()

    def write(self, data: list[Video]):
        self.cursor.executemany("""
            INSERT INTO videos(
                channel_username, video_id, video_href
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING
        """, (v.to_tuple() for v in data)
        )
        self.conn.commit()

    def __exit__(self, *args, **kwargs):
        self.cursor.close()
        self.conn.close()
