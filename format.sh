#!/usr/bin/bash

PROJECT_NAME=bookkeeper
poetry run black --line-length 80 $PROJECT_NAME
