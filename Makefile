install-deps:
	python -m pip install --upgrade pip
	python -m pip install flake8 pytest
	pip install -r requirements.txt

run-tests:
	export PYTHONPATH='./'
	pytest tests/

run-linter:
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
