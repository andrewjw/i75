#!/bin/bash

${COVERAGE:-coverage} run test.py

let R=$?

${COVERAGE:-coverage} report

${COVERAGE:-coverage} html

exit $R
