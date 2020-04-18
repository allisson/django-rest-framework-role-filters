.PHONY: clean-pyc

default: test

clean-pyc:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@find . -iname '.coverage' -delete
	@rm -rf htmlcov/

clean-dist:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info

clean: clean-pyc clean-dist

lint:
	flake8 --ignore=E501,W503 **/*.py
	isort --check-only **/*.py
	black --check --quiet **/*.py

test:
	cd testproject && pytest

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel

release: dist
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	twine upload dist/*
