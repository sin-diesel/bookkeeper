PROJECT_NAME=bookkeeper

poetry run pylint $PROJECT_NAME
poetry run mypy --strict --no-site-packages $PROJECT_NAME
poetry run flake8 $PROJECT_NAME
