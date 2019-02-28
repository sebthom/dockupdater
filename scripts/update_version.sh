#!/usr/bin/env bash

if [ -z ${TRAVIS_TAG} ]; then
    sed -i -E "s#VERSION = \".*\"#VERSION = \"${TRAVIS_TAG}\"#g"
fi
