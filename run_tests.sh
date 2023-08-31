#!/bin/bash

PYTHONPATH=./i75/emulated:$PYTHONPATH ${COVERAGE:-coverage} run test.py

let R=$?

${COVERAGE:-coverage} report

${COVERAGE:-coverage} html

exit $R
