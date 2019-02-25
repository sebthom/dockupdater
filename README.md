[![Release](https://img.shields.io/github/release/docupdater/docupdater.svg?style=flat-square)](https://hub.docker.com/r/docupdater/docupdater/)
[![Travis (.org)](https://img.shields.io/travis/docupdater/docupdater.svg)](https://travis-ci.org/docupdater/docupdater/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/docupdater.svg?style=flat-square)](https://pypi.org/project/docupdater/)
[![Python Version](https://img.shields.io/pypi/pyversions/docupdater.svg?style=flat-square)](https://pypi.org/project/docupdater/)
[![Docker Pulls](https://img.shields.io/docker/pulls/docupdater/docupdater.svg?style=flat-square)](https://hub.docker.com/r/docupdater/docupdater/)
[![Layers](https://images.microbadger.com/badges/image/docupdater/docupdater.svg)](https://microbadger.com/images/docupdater/docupdater)  

Automatically keep your docker services and your docker containers up-to-date with the latest version.

A fork of Ouroboros.

## Overview

Docupdater will monitor (all or specified by a label) running docker containers and running service (in docker swarm) and update them to the (latest or tagged) available image in the remote registry.

- Push your image to your registry and simply wait your defined interval for docupdater to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Use with docker swarm to update services on the latest available version
- Limit your server SSH access
- Useful to keep 3rd party container up-to-date

## Getting Started

More detailed usage and configuration can be found on [the docs](https://github.com/docupdater/docupdater/blob/master/docs/Home.md).

### Docker

Docupdater is deployed via docker image in a standalone container like so:

```bash
docker run -d --name docupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docupdater/docupdater
```

or via a stack file (docker swarm):

```bash
version: "3.6"

services:
  docupdater:
    image: docupdater/docupdater
```

> This is image is compatible for amd64, arm32, and arm64 CPU architectures

## Examples
Per-command and scenario examples can be found in the [docs](https://github.com/docupdater/docupdater/blob/master/docs/Home.md).

## Contributing

All contributions are welcome!
