[![Build Status](https://jenkins.cajun.pro/buildStatus/icon?job=pyupdater/master)](https://jenkins.cajun.pro/job/pyupdater/job/master/)
[![Release](https://img.shields.io/github/release/pypyupdater/pyupdater.svg?style=flat-square)](https://hub.docker.com/r/pypyupdater/pyupdater/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/pyupdater-cli.svg?style=flat-square)](https://pypi.org/project/pyupdater-cli/)
[![Python Version](https://img.shields.io/pypi/pyversions/pyupdater-cli.svg?style=flat-square)](https://pypi.org/project/pyupdater-cli/)
[![Docker Pulls](https://img.shields.io/docker/pulls/pypyupdater/pyupdater.svg?style=flat-square)](https://hub.docker.com/r/pypyupdater/pyupdater/)
[![Layers](https://images.microbadger.com/badges/image/pypyupdater/pyupdater.svg)](https://microbadger.com/images/pypyupdater/pyupdater)  

Automatically update your running Docker containers to the latest available image.

A python-based successor to [watchtower](https://github.com/v2tec/watchtower)

## Overview

pyupdater will monitor (all or specified) running docker containers and update them to the (latest or tagged) available image in the remote registry. The updated container uses the same tag and parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc.

- Push your image to your registry and simply wait your defined interval for pyupdater to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Serve metrics for trend monitoring (Currently: Prometheus/Influxdb)
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs
- `docker-compose pull && docker-compose up -d` is for fancier scrubs

## Getting Started

More detailed usage and configuration can be found on [the wiki](https://github.com/pypyupdater/pyupdater/wiki).

### Docker

pyupdater is deployed via docker image like so:

```bash
docker run -d --name pyupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pypyupdater/pyupdater
```

> This is image is compatible for amd64, arm32, and arm64 CPU architectures

or via `docker-compose`:

[Official Example](https://github.com/pypyupdater/pyupdater/blob/master/docker-compose.yml)

### Pip

pyupdater can also be installed via `pip`:

```bash
pip install pyupdater-cli
```

And can then be invoked using the `pyupdater` command:

```bash
$ pyupdater --interval 300 --log-level debug
```

> This can be useful if you would like to create a `systemd` service or similar daemon that doesn't run in a container

## Examples
Per-command and scenario examples can be found in the [wiki](https://github.com/pypyupdater/pyupdater/wiki/Usage)

## Contributing

All contributions are welcome! Contributing guidelines are in the works
