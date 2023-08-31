#!/bin/bash

set -e

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy -m i75

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy -m examples

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy -m tests

${PYCODESTYLE:-pycodestyle} i75/ examples/ tests/
