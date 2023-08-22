#!/bin/bash

set -e

MYPYPATH=./stubs:$MYPYPATH mypy -m interstate75wrapper

MYPYPATH=./stubs:$MYPYPATH mypy -m examples

${PYCODESTYLE:-pycodestyle} interstate75wrapper/ examples/
