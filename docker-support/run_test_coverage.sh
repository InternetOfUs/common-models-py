#!/bin/bash


# The variable TEST_DIR_PATH hosts the path to the tests folder.
TEST_DIR_PATH=$1
if [[ -z "${TEST_DIR_PATH}" ]]; then
    TEST_DIR_PATH=/scripts/test
fi

# The variable COV_DIR_PATH hosts the path to the folder the coverage should be matched against.
COV_DIR_PATH=$2
if [[ -z "${COV_DIR_PATH}" ]]; then
    COV_DIR_PATH=/scripts
fi
echo "Running coverage for for folder [${COV_DIR_PATH}] and tests in [${TEST_DIR_PATH}]."

pytest --cov=${COV_DIR_PATH} --cov-config=.coveragerc ${TEST_DIR_PATH} --junitxml=report.xml

