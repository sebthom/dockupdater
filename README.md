[![Release](https://img.shields.io/github/release/docupdater/docupdater.svg?style=flat-square)](https://hub.docker.com/r/docupdater/docupdater/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/docupdater-cli.svg?style=flat-square)](https://pypi.org/project/docupdater-cli/)
[![Python Version](https://img.shields.io/pypi/pyversions/pyupdater-cli.svg?style=flat-square)](https://pypi.org/project/pyupdater-cli/)
[![Docker Pulls](https://img.shields.io/docker/pulls/docupdater/docupdater.svg?style=flat-square)](https://hub.docker.com/r/docupdater/docupdater/)
[![Layers](https://images.microbadger.com/badges/image/docupdater/docupdater.svg)](https://microbadger.com/images/docupdater/docupdater)  

Automatically update your running Docker containers and service to the latest available image.

A fork of Ouroboros.

## Overview

Docupdater will monitor (all or specified) running docker containers and running service (in swarm) and update them to the (latest or tagged) available image in the remote registry.

- Push your image to your registry and simply wait your defined interval for docupdater to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Limit your server ssh access

## Getting Started

More detailed usage and configuration can be found on [the docs](https://github.com/docupdater/docupdater/blob/master/docs/Home.md).

### Docker

docupdater is deployed via docker image like so:

```bash
docker run -d --name pyupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pypyupdater/pyupdater
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
Per-command and scenario examples can be found in the [docs](https://github.com/docupdater/docupdater/blob/master/docs/Options.md)

## Contributing

All contributions are welcome!
