#!/usr/bin/env bash

docker tag dockupdater/dockupdater:$TRAVIS_BRANCH-amd64 dockupdater/dockupdater:$TRAVIS_TAG-amd64
docker tag dockupdater/dockupdater:$TRAVIS_BRANCH-arm dockupdater/dockupdater:$TRAVIS_TAG-arm
docker tag dockupdater/dockupdater:$TRAVIS_BRANCH-arm64 dockupdater/dockupdater:$TRAVIS_TAG-arm64

docker push dockupdater/dockupdater:$TRAVIS_TAG-amd64
docker push dockupdater/dockupdater:$TRAVIS_TAG-arm
docker push dockupdater/dockupdater:$TRAVIS_TAG-arm64

docker manifest create dockupdater/dockupdater:$TRAVIS_TAG dockupdater/dockupdater:$TRAVIS_TAG-amd64 dockupdater/dockupdater:$TRAVIS_TAG-arm64 dockupdater/dockupdater:$TRAVIS_TAG-arm
docker manifest inspect dockupdater/dockupdater:$TRAVIS_TAG
docker manifest push dockupdater/dockupdater:$TRAVIS_TAG

docker tag dockupdater/dockupdater:$TRAVIS_BRANCH-amd64 dockupdater/dockupdater:latest-amd64
docker tag dockupdater/dockupdater:$TRAVIS_BRANCH-arm dockupdater/dockupdater:latest-arm
docker tag dockupdater/dockupdater:$TRAVIS_BRANCH-arm64 dockupdater/dockupdater:latest-arm64

docker push dockupdater/dockupdater:latest-amd64
docker push dockupdater/dockupdater:latest-arm
docker push dockupdater/dockupdater:latest-arm64

docker manifest create dockupdater/dockupdater:latest dockupdater/dockupdater:latest-amd64 dockupdater/dockupdater:latest-arm64 dockupdater/dockupdater:latest-arm
docker manifest inspect dockupdater/dockupdater:latest
docker manifest push dockupdater/dockupdater:latest
