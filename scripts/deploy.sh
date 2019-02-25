#!/usr/bin/env bash

docker push docupdater/docupdater:$TRAVIS_BRANCH-amd64
docker push docupdater/docupdater:$TRAVIS_BRANCH-arm64
docker push docupdater/docupdater:$TRAVIS_BRANCH-arm

docker manifest create docupdater/docupdater:$TRAVIS_BRANCH docupdater/docupdater:$TRAVIS_BRANCH-amd64 docupdater/docupdater:$TRAVIS_BRANCH-arm64 docupdater/docupdater:$TRAVIS_BRANCH-arm
docker manifest inspect docupdater/docupdater:$TRAVIS_BRANCH
docker manifest push docupdater/docupdater:$TRAVIS_BRANCH
