.PHONY: help tests ruff qc test stub
default: help

define PYTEST_TEMPLATE
if __name__ == "__main__":
    import pytest
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))

endef
define DAY_STUB
import advent_of_code.utils as utils


def main():
    with utils.contents() as contents:
        ...
        # TODO


if __name__ == "__main__":
    main()

endef
tests: # Run tests using pytest.
	@pytest --cov advent_of_code --cov-report term-missing

ruff: # Format the python files using ruff.
	@ruff check --fix advent_of_code && ruff format advent_of_code

qc: ruff tests # Run formatting and tests

export PYTEST_TEMPLATE 
test: # Create a test stub file and add to git
	@[ -z "${name}" ] &&  >&2 echo "Command missing name argument. Usage: 'make test name=test_hello'" && exit 1 || export outfile="tests/test_$(shell echo '${name}' | sed -E 's/(^test_|^)(.*?)($$|\.py$$)/\2/g' ).py" && [ -f "$$outfile" ] && echo "File $$outfile exists, renaming..." && mv $$outfile $$outfile.old; echo "$$PYTEST_TEMPLATE" > $$outfile && git add $$outfile

export DAY_STUB 
stub: #Create a stub for a day
	@export outfile="advent_of_code/day_$(shell printf %02d ${day}).py" && [ -f "$$outfile" ] &&  >&2 echo "File $$outfile already exists" && exit 1 || echo "$$DAY_STUB" > $$outfile && git add $$outfile

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m\n\t$$(echo $$l | cut -f 2- -d'#')\n"; done
