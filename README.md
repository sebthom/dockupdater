# Docker + Updater = Docupdater

[![Release](https://img.shields.io/github/release/docupdater/docupdater.svg?style=flat-square)](https://hub.docker.com/r/docupdater/docupdater/)
[![Travis](https://img.shields.io/travis/docupdater/docupdater/master.svg)](https://travis-ci.org/docupdater/docupdater/)
[![Codecov](https://img.shields.io/codecov/c/github/docupdater/docupdater/master.svg)](https://codecov.io/gh/docupdater/docupdater)
[![Python Version](https://img.shields.io/pypi/pyversions/docupdater.svg?style=flat-square)](https://pypi.org/project/docupdater/)
[![Pypi Version](https://img.shields.io/pypi/v/docupdater.svg?style=flat-square)](https://pypi.org/project/docupdater/)
[![Latest version](https://images.microbadger.com/badges/version/docupdater/docupdater.svg)](https://microbadger.com/images/docupdater/docupdater)
[![Docker Pulls](https://img.shields.io/docker/pulls/docupdater/docupdater.svg?style=flat-square)](https://hub.docker.com/r/docupdater/docupdater/)
[![Layers](https://images.microbadger.com/badges/image/docupdater/docupdater.svg)](https://microbadger.com/images/docupdater/docupdater)  

Automatically keep your docker services and your docker containers up-to-date with the latest version.

## Overview

**Docupdater** will monitor (all or specified by a label) running docker containers and running service (in Docker swarm) and update them to the (latest or tagged) available image in the remote registry.

- Push your image to your registry and simply wait your defined interval for docupdater to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Use with Docker swarm to update services on the latest available version
- Limit your server SSH access
- Useful to keep 3rd party container up-to-date

## Getting Started

More detailed usage and configuration can be found on [the docs](https://docupdater.github.io/docupdater/).

### Docker container

**Docupdater** is deployed via docker image in a standalone container like so:

```bash
docker run -d --name docupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docupdater/docupdater
```

> This is image is compatible for amd64, arm32, and arm64 CPU architectures

### Docker swarm (service)

**Docupdater** can be deploy on a service like that:

```bash
version: "3.6"

services:
  docupdater:
    image: docupdater/docupdater
    deploy:
      placement:
        constraints:
          - node.role == manager
```

> Docupdater need to run on a manager node

## Getting helps

* [Issues list](https://github.com/docupdater/docupdater/issues)
* [Documentation](https://docupdater.github.io/docupdater/)
* [Releases and changelogs](https://github.com/docupdater/docupdater/releases)
* [Frequently Asked Questions](https://docupdater.github.io/docupdater/Frequently-Asked-Questions.md)

## Reporting bugs and contributing

All contributions are welcome!

* Want to report a bug or request a feature? Please open [an issue](https://github.com/docupdater/docupdater/issues/new).
* Want to help us? Your contribution and your pull request are welcome. We need all the help we can get!
