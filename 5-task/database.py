import os
import psycopg2

from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "quotes_db"),
    "user": os.getenv("DB_USER", "parser_user"),
    "password": os.getenv("DB_PASSWORD", "mysecret123")
}

print(f"Подключение к БД: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")


@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_table():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id SERIAL PRIMARY KEY,
                    url_source VARCHAR(500),
                    quote TEXT NOT NULL,
                    author VARCHAR(255),
                    tags TEXT,
                    tags_count INTEGER,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
    print("Таблица создана")


def save_quotes_to_db(quotes_data, source_url):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for quote in quotes_data:
                cur.execute("""
                    INSERT INTO quotes (url_source, quote, author, tags, tags_count)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    source_url,
                    quote["quote"],
                    quote["author"],
                    quote["tags"],
                    quote["tags_count"]
                ))
    print(f"✓ Сохранено {len(quotes_data)} цитат в БД")


def get_all_quotes():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM quotes ORDER BY id DESC")
            rows = cur.fetchall()
            for row in rows:
                if 'created_at' in row and row['created_at']:
                    row['created_at'] = row['created_at'].isoformat()
            return rows


def get_quotes_count():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM quotes")
            return cur.fetchone()[0]


def clear_quotes_table():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM quotes")
    print("Таблица очищена")
