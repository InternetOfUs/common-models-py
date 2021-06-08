#!/bin/bash
python -m unittest discover test

if [[ $? != 0 ]]; then
    echo "Error: Tests are failing."
    exit 1
fi

