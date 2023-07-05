from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators
import datetime
import requests


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def get_checks_id():
    with conn.cursor() as curs:
        curs.execute("SELECT id FROM url_checks;")
        checks_id = curs.fetchall()
    return checks_id


def get_checks(id_):
    with conn.cursor() as curs:
        curs.execute(f"SELECT * FROM url_checks WHERE url_id = '{id_}' ORDER BY id DESC;")
        need_checks = curs.fetchall()
        return need_checks


def making_check(id_, answer):
    new_date = datetime.date.today()
    checks_id = get_checks_id()
    if checks_id == []:
        new_id = 1
    else:
        for ids in checks_id:
            new_id = max(ids) + 1
    with conn.cursor() as curs:
        curs.execute(f"INSERT INTO url_checks (id, url_id, status_code, created_at) VALUES ('{new_id}', '{id_}', '{answer}', '{new_date}');")
        curs.execute(f"UPDATE all_urls SET check_date = '{new_date}', answer = '{answer}' WHERE id = '{id_}';")

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
        curs.execute(f"SELECT * FROM all_urls ORDER BY id DESC;")
        getted_urls = curs.fetchall()
        return getted_urls


def url_db_add(cutted_url):
    new_date = datetime.datetime.today()
    all_ids = get_id()
    if all_ids == []:
        new_id = 1
    else:
        for ids in all_ids:
            new_id = max(ids) + 1
    with conn.cursor() as curs:
        curs.execute(f"INSERT INTO urls (id, name, created_at) VALUES ('{new_id}', '{cutted_url}', '{new_date}');")
        curs.execute(f"INSERT INTO all_urls (id, url_name) VALUES ('{new_id}', '{cutted_url}');")
        curs.execute(f"SELECT * FROM urls WHERE name = '{cutted_url}';")
        new_note = curs.fetchone()
    return new_note


def cutting_url(address):
    if validators.url(address) and len(address) <= 255:
        x = urlparse(address)
        cutted_url = (f"{x.scheme}://{x.hostname}")
        return cutted_url


@app.route('/')
def analyzer():
    return render_template(
            'index.html'
            )


@app.post('/urls')
def urls_post():
    address = request.form.get('url')
    cutted_url = cutting_url(address)
    urls = url_db()
    if cutted_url:
        for i in urls:
            if cutted_url in i:
                flash('Страница уже существует', 'info')
                id_ = i[0]
                return redirect(url_for('add_url', id=id_))
        
        new_note = url_db_add(cutted_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('add_url', id=new_note[0]))

    flash('Некорректный URL', 'error')
    messages=get_flashed_messages(with_categories=True)
    return render_template('index.html', incorrect_url=address, messages=messages)


@app.get('/urls')
def urls_get():
    all_urls = get_all_urls()
    return render_template('all_pages.html', all_urls=all_urls)


@app.route('/urls/<id>')
def add_url(id):
    messages = get_flashed_messages(with_categories=True)
    cur_url = get_url(id)
    cur_checks = get_checks(id)
    return render_template('page.html', messages=messages, urls=cur_url, checks=cur_checks)


@app.post('/urls/<id>/checks')
def check_url(id):
    cur_url = get_url(id)
    req = requests.get(cur_url[1])
    status_code = req.status_code
    if status_code != 200:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('add_url', id=id))
    flash('Страница успешно проверена', 'success')
    making_check(id, status_code)
    return redirect(url_for('add_url', id=id))
