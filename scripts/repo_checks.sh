#!/usr/bin/env zsh

poetry run black . && poetry run isort . && poetry run flake8 && poetry run mypy . && poetry run coverage run -m pytest && poetry run coverage report -m
