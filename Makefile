HYPOTHESIS_PROFILE=slow

SOURCES=interfax tests setup.py

test:
	py.test

format:
	isort -rc $(SOURCES)
	find $(SOURCES) -name '*.py' | xargs pyformat --in-place

lint:
	flake8 $(SOURCES) --exclude=_compat.py

ci:
	tox

release:
	python scripts/release.py

.PHONY: test ci lint format release