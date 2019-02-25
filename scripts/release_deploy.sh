#!/usr/bin/env bash

./deploy.sh

docker tag docupdater/docupdater:$TRAVIS_BRANCH docupdater/docupdater:latest
docker tag docupdater/docupdater:$TRAVIS_BRANCH docupdater/docupdater:$TRAVIS_TAG
docker push docupdater/docupdater:$TRAVIS_TAG
docker push docupdater/docupdater:latest
