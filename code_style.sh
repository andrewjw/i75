#!/bin/bash

set -e

${PYCODESTYLE:-pycodestyle} interstate75wrapper/ examples/

MYPYPATH=./stubs:$MYPYPATH mypy -m interstate75wrapper

MYPYPATH=./stubs:$MYPYPATH mypy -m examples
