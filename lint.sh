PROJECT_NAME=bookkeeper
poetry run pylint --fail-under=9 $PROJECT_NAME
poetry run mypy --strict $PROJECT_NAME
poetry run flake8 $PROJECT_NAME
