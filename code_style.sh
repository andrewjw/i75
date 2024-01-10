#!/bin/bash

set -e

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy bin/i75

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy bin/i75-convert-image

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy -m i75

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy -m examples

MYPYPATH=./stubs:./i75/emulated:$MYPYPATH mypy -m tests

${PYCODESTYLE:-pycodestyle} bin/ i75/ examples/ tests/
