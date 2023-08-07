

doc:
	python -m sphinx ./docs ./docs/_build

test:
	python -m pytest -k 'not api'