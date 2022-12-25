# POETRY COMMANDS 
.PHONY: install pbuild black pytest run requirements

install:
	poetry install

pbuild: install
	poetry build

black:
    poetry run sort .
	poetry run black .

pytest:
	poetry run pytest --cov=./tests --black -rAP 

run:
	poetry run python main.py
	
requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt