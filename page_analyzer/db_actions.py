import psycopg2
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_checks_id():
    with conn.cursor() as curs:
        curs.execute("SELECT id FROM url_checks;")
        checks_id = curs.fetchall()
    return checks_id


def get_checks(id_):
    with conn.cursor() as curs:
        curs.execute(f"""SELECT * FROM url_checks
                WHERE url_id = '{id_}'
                ORDER BY id DESC;""")
        need_checks = curs.fetchall()
    return need_checks


def making_check(id_, answer, h1, title, description):
    new_date = datetime.date.today()
    checks_id = get_checks_id()

    if checks_id == []:
        new_id = 1
    else:
        for ids in checks_id:
            new_id = max(ids) + 1

    with conn.cursor() as curs:

        curs.execute(f"""INSERT INTO url_checks (id, url_id, status_code,
        h1, title, description, created_at)
        VALUES ('{new_id}', '{id_}', '{answer}',
        '{h1}', '{title}', '{description}', '{new_date}');""")

        curs.execute(f"""UPDATE all_urls
        SET check_date = '{new_date}', answer = '{answer}'
        WHERE id = '{id_}';""")


def get_id():
    with conn.cursor() as curs:
        curs.execute("SELECT id FROM urls;")
        all_ids = curs.fetchall()
    return all_ids


def url_db():
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls;")
        urls = curs.fetchall()
    return urls


def get_url(id_):
    with conn.cursor() as curs:
        curs.execute(f"SELECT * FROM urls WHERE id = '{id_}';")
        need_url = curs.fetchone()
    return need_url


def get_all_urls():
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM all_urls ORDER BY id DESC;")
        getted_urls = curs.fetchall()
    return getted_urls


def url_db_add(cutted_url):
    new_date = datetime.date.today()
    all_ids = get_id()

    if all_ids == []:
        new_id = 1
    else:
        for ids in all_ids:
            new_id = max(ids) + 1

    with conn.cursor() as curs:
        curs.execute(f"""INSERT INTO urls (id, name, created_at)
                VALUES ('{new_id}', '{cutted_url}', '{new_date}');""")
        curs.execute(f"""INSERT INTO all_urls (id, url_name)
                VALUES ('{new_id}', '{cutted_url}');""")
        curs.execute(f"SELECT * FROM urls WHERE name = '{cutted_url}';")
        new_note = curs.fetchone()
    return new_note
