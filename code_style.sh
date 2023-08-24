#!/bin/bash

set -e

MYPYPATH=./stubs:$MYPYPATH mypy -m interstate75wrapper

MYPYPATH=./stubs:$MYPYPATH mypy -m examples

MYPYPATH=./stubs:$MYPYPATH mypy -m tests

${PYCODESTYLE:-pycodestyle} interstate75wrapper/ examples/ tests/
