.PHONY: help tests ruff qc
default: help

tests: # Run tests using pytest.
	@pytest --cov advent_of_code --cov-report term-missing

ruff: # Format the python files using ruff.
	@ruff check --fix advent_of_code && ruff format advent_of_code

qc: ruff tests

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m\n\t$$(echo $$l | cut -f 2- -d'#')\n"; done
