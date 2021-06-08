#!/bin/bash

DEFAULT_VERSION="latest"

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

BUILD=0
TEST=0
DELETE_IF_FAILED=0
SAVE_IMAGE_TO_TARGZ=0
PUSH_IMAGE=0
TEST_COVERAGE=0

usage() {
  echo '''Usage: ...

  runner.sh [-flags] [imageVersion]

  -b  build image
  -t  run tests within image
  -d  delete image if tests fail
  -s  save image to tar.gz
  -p  push image to registry
  -i  pull image from registry
  -c  test coverage

Example:

  ./runner.sh -btp 1.0.0
  '''
}

args=`getopt btdspc $*`
# you should not use `getopt abo: "$@"` since that would parse
# the arguments differently from what the set command below does.
if [[ $? != 0 ]]
then
  usage
  exit 2
fi
set -- ${args}
# You cannot use the set command with a backquoted getopt directly,
# since the exit code from getopt would be shadowed by those of set,
# which is zero by definition.
for i do
  case "$i" in
     -b)
       BUILD=1
       shift;;
     -t)
       TEST=1
       shift;;
     -d)
       DELETE_IF_FAILED=1
       shift;;
     -s)
       SAVE_IMAGE_TO_TARGZ=1
       shift;;
     -p)
       PUSH_IMAGE=1
       shift;;
     -c)
       TEST_COVERAGE=1
       shift;;
  esac
done

# Identifying build version
VERSION=$2
if [[ -z "${VERSION}" ]]; then
    VERSION=${DEFAULT_VERSION}
    echo "Version not specified: building with default version [${VERSION}]."
else
    echo "Using specified version [${VERSION}]."
fi

# Exporting image name for the build and test scripts
REGISTRY=registry.u-hopper.com
export IMAGE_NAME=project/component:${VERSION}
export REGISTRY=${REGISTRY}

# Build step
if [[ ${BUILD} == 1 ]]; then
  echo "Building image."
  ${SCRIPT_DIR}/build_image.sh

  if [[ $? != 0 ]]; then
    echo "Error: Build Failed"
    exit 1
  fi

  # Save step
  if [[ ${SAVE_IMAGE_TO_TARGZ} == 1 ]]; then
    echo "Saving image to docker_image.tar.gz."
    docker save ${REGISTRY}/${IMAGE_NAME} | gzip > docker_image.tar.gz
  fi
fi

# Test step
if [[ ${TEST} == 1 ]]; then
  echo "Running tests."
  ${SCRIPT_DIR}/test.sh

  if [[ $? != 0 ]]; then
      echo "Error: One or more tests are failed."
      if [[ ${DELETE_IF_FAILED} == 1 ]]; then
        docker rmi ${REGISTRY}/${IMAGE_NAME}  # TODO check if correct
      fi
      exit 1
  fi
fi

# Test coverage step
if [[ ${TEST_COVERAGE} == 1 ]]; then
  echo "Running test coverage."
  ${SCRIPT_DIR}/test_coverage.sh

  if [[ $? != 0 ]]; then
      echo "Error: Could not verify test coverage."
      if [[ ${DELETE_IF_FAILED} == 1 ]]; then
        docker rmi ${REGISTRY}/${IMAGE_NAME}  # TODO check if correct
      fi
      exit 1
  fi
fi

if [[ ${PUSH_IMAGE} == 1 ]]; then
  echo "Pushing image to registry"
  docker push ${REGISTRY}/${IMAGE_NAME}
fi

if [[ ${BUILD} == 0 ]] && [[ ${TEST} == 0 ]] && [[ ${PUSH_IMAGE} == 0 ]] && [[ ${TEST_COVERAGE} == 0 ]]; then
  echo "Need to specify at least one parameter"
  usage
  exit 1
fi
