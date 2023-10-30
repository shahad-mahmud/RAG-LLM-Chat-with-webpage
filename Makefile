setup:
	bash setup.sh

pytest:
	pytest --cov-report term --cov=src .

format:
	isort .
	black .
	flake8

pre-commit:
	pre-commit run --all-files

check: format pre-commit pytest

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	rm -rf .coverage*
