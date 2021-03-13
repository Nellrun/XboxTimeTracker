install-deps:
	python -m pip install --upgrade pip
	python -m pip install flake8 pytest
	pip install -r requirements.txt

run-tests:
	export PYTHONPATH='./'; pytest

run-linter:
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

start-cron-session:
	export PYTHONPATH='./'; python crons/session_cron.py

start-cron-daily-stats:
	export PYTHONPATH='./'; python crons/daily_stats.py

start-bot:
	python app.py
