#!/bin/bash

set -e

MYPYPATH=./stubs:$MYPYPATH mypy -m i75

MYPYPATH=./stubs:$MYPYPATH mypy -m examples

MYPYPATH=./stubs:$MYPYPATH mypy -m tests

${PYCODESTYLE:-pycodestyle} i75/ examples/ tests/
