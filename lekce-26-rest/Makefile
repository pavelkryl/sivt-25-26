.PHONY: prepare run

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

help:
	echo "prepare or run?"

prepare:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install fastapi uvicorn pydantic

run:
	$(PYTHON) student_registr_server.py