#!/bin/bash

DEFAULT_VERSION="latest"


clean () {
    echo "Cleaning."
    rm -R -f ${SCRIPT_DIR}/src
    rm -R -f ${SCRIPT_DIR}/documentation
    rm -R ${SCRIPT_DIR}/requirements.txt

    rm -R ${SCRIPT_DIR}/test

}

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PROJECT_DIR=${SCRIPT_DIR}/..

mkdir ${SCRIPT_DIR}/src
cp -R ${PROJECT_DIR}/src/* ${SCRIPT_DIR}/src
mkdir ${SCRIPT_DIR}/documentation
cp -R ${PROJECT_DIR}/documentation/* ${SCRIPT_DIR}/documentation
cp ${PROJECT_DIR}/requirements.txt ${SCRIPT_DIR}


mkdir ${SCRIPT_DIR}/test
cp -R ${PROJECT_DIR}/test/* ${SCRIPT_DIR}/test


# Building image
GIT_REF=`git rev-parse --short HEAD`
if [[ -z "${PIP_CONF_DOCKER}" ]]; then
    export PIP_CONF_DOCKER=`cat ~/.config/pip/pip.conf`
fi
docker build --build-arg GIT_REF=${GIT_REF} --build-arg PIP_CONF_DOCKER --cache-from ${REGISTRY}/${IMAGE_NAME} -t ${IMAGE_NAME} ${SCRIPT_DIR}
if [[ $? == 0 ]]; then
    echo "Build successful: ${IMAGE_NAME}."

    # Tagging images for registry
    echo "Tagging image for push to ${REGISTRY}."
    docker tag ${IMAGE_NAME} ${REGISTRY}/${IMAGE_NAME}
    echo "Image can be pushed with:"
    echo "  docker push ${REGISTRY}/${IMAGE_NAME}"

    # Cleaning
    clean

    exit 0

else
    echo "Error: Build failed for ${IMAGE_NAME}."

    # Cleaning
    clean

    exit 1
fi
