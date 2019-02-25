#!/usr/bin/env bash

docker tag docupdater/docupdater:$TRAVIS_BRANCH-amd64 docupdater/docupdater:latest-amd64 docupdater/docupdater:$TRAVIS_TAG-amd64
docker tag docupdater/docupdater:$TRAVIS_BRANCH-arm docupdater/docupdater:latest-arm docupdater/docupdater:$TRAVIS_TAG-arm
docker tag docupdater/docupdater:$TRAVIS_BRANCH-arm64 docupdater/docupdater:latest-arm64 docupdater/docupdater:$TRAVIS_TAG-arm64

docker manifest create docupdater/docupdater:$TRAVIS_TAG docupdater/docupdater:$TRAVIS_TAG-amd64 docupdater/docupdater:$TRAVIS_TAG-arm64 docupdater/docupdater:$TRAVIS_TAG-arm
docker manifest inspect docupdater/docupdater:$TRAVIS_TAG
docker manifest push docupdater/docupdater:$TRAVIS_TAG

docker manifest create docupdater/docupdater:latest docupdater/docupdater:latest-amd64 docupdater/docupdater:latest-arm64 docupdater/docupdater:latest-arm
docker manifest inspect docupdater/docupdater:latest
docker manifest push docupdater/docupdater:latest
