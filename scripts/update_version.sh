#!/usr/bin/env bash

if [[ "${TRAVIS_TAG}" != "" ]]; then
    sed -i -E "s#VERSION = \".*\"#VERSION = \"${TRAVIS_TAG}\"#g"
fi
