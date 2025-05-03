#!/bin/bash

source .venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$(pwd)

python -m pytest tests/src/shared/ -v --cov=src/shared --cov-report=xml
