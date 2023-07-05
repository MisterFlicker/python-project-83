from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for
import os
from dotenv import load_dotenv
import requests
from page_analyzer.parser import parsing
from page_analyzer.cutter import cutting_url
from page_analyzer.db_actions import get_checks_id, get_checks, making_check, get_id, url_db, get_url, get_all_urls, url_db_add


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


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

    parsed_url = parsing(cur_url[1])

    h1 = parsed_url.get('h1', '')
    title = parsed_url.get('title', '')
    description = parsed_url.get('description', '')

    flash('Страница успешно проверена', 'success')
    making_check(id, status_code, h1, title, description)
    return redirect(url_for('add_url', id=id))
