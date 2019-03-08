#!/usr/bin/env bash

docker push dockupdater/dockupdater:$TRAVIS_BRANCH-amd64
docker push dockupdater/dockupdater:$TRAVIS_BRANCH-arm64
docker push dockupdater/dockupdater:$TRAVIS_BRANCH-arm

docker manifest create dockupdater/dockupdater:$TRAVIS_BRANCH dockupdater/dockupdater:$TRAVIS_BRANCH-amd64 dockupdater/dockupdater:$TRAVIS_BRANCH-arm64 dockupdater/dockupdater:$TRAVIS_BRANCH-arm
docker manifest inspect dockupdater/dockupdater:$TRAVIS_BRANCH
docker manifest push dockupdater/dockupdater:$TRAVIS_BRANCH
