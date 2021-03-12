install-deps:
	python -m pip install --upgrade pip
	python -m pip install flake8 pytest
	pip install -r requirements.txt

run-tests:
	export PYTHONPATH='./'
	pytest tests/
