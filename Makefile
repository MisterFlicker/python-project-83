install: # создание или обновление виртуального окружения
	poetry install

build: # выполнение сборки пакета
	poetry build

publish: # отладка публикации
	poetry publish --dry-run

package-install-f: # установка пакета в систему (по факту переустановка)
	pip install --user --force-reinstall dist/*.whl

package-install: # установка пакета в систему
	python3 -m pip install --user dist/*.whl

lint: # проверка gendiff по линтеру flake8
	poetry run flake8 gendiff

test: # проверка gendiff по pytest
	poetry run pytest

selfcheck:
	poetry check

test-coverage: # проверка по покрытию теста
	poetry run pytest --cov=gendiff --cov-report xml tests/

run: #старт
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start: #gunicorn
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
