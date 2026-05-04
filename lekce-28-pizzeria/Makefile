prepare:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt


run:
	# the documentation lives at http://localhost:8000/docs
	. .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0

