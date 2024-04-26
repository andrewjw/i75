#!/bin/bash

set -e

MYPYPATH=./i75/stubs:./i75/emulated:$MYPYPATH mypy bin/i75

MYPYPATH=./i75/stubs:./i75/emulated:$MYPYPATH mypy bin/i75-convert-image

MYPYPATH=./i75/stubs:./i75/emulated:$MYPYPATH mypy -m i75

MYPYPATH=./i75/stubs:./i75/emulated:$MYPYPATH mypy -p examples

MYPYPATH=./i75/stubs:./i75/emulated:$MYPYPATH mypy -m tests

${PYCODESTYLE:-pycodestyle} bin/ i75/ examples/ tests/
