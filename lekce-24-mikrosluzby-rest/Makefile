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
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) --host 0.0.0.0 rest_api:app --reload

run-obj:
	$(UVICORN) --host 0.0.0.0 obj_rest_api:app --reload
