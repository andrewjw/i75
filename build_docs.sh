#!/bin/bash

PYTHONPATH=i75/emulated:$PYTHONPATH sphinx-build  -b html docs/ htmldocs/
