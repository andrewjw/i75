#!/bin/bash

set -e

${PYCODESTYLE:-pycodestyle} interstate75-wrapper/ tests/

MYPYPATH=./stubs:$MYPYPATH mypy -m interstate75-wrapper

MYPYPATH=./stubs:$MYPYPATH mypy -m tests
