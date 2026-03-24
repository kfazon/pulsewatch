venv: .venv/bin/activate

.venv/bin/activate:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && python3 -m pip install -r requirements.txt && playwright install
test: venv
	. .venv/bin/activate && python -m pytest tests/ -v
capture: venv
	. .venv/bin/activate && python -m pulsewatch capture --config sample_targets.yaml
lint: venv
	. .venv/bin/activate && python -m ruff check . && python -m ruff format --check .
format: venv
	. .venv/bin/activate && python -m ruff format .
