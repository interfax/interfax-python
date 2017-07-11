HYPOTHESIS_PROFILE=slow

SOURCES=interfax tests setup.py

BINSTUBS ?= isort make pytest python tox pyformat flake8

test:
	py.test

format:
	isort -rc $(SOURCES)
	find $(SOURCES) -name '*.py' | xargs pyformat --in-place

lint:
	flake8 $(SOURCES) --exclude=_compat.py

binstubs:
	@rm -rf .bin
	@mkdir .bin
	@for NAME in $(BINSTUBS); do \
		printf '#!/bin/sh\n\ndocker-compose run --no-deps --rm default $$(basename $$0) $$@' > .bin/$$NAME; \
		chmod +x .bin/$$NAME; \
	done
	@echo $(BINSTUBS)

ci:
	tox

release:
	python scripts/release.py

.PHONY: test ci lint binstubs format release