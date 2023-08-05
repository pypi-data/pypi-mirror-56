#!/bin/bash
# This runs in docker to pin our requirements files.
SUFFIX=${SUFFIX:-txt}

pip install --upgrade pip
pip install pip-compile-multi

pip-compile-multi -g base -g test -o "$SUFFIX"
