Automatically keep your docker services and your docker containers up-to-date with the latest version.

## Table of Contents

- [Options usage](Options.md)
- [Customize usage with labels](Labels.md)
- [Private Registries](Private-Registries.md)
- [Customized Scheduling](Customized-Scheduling.md)
- [Notifications](Notifications.md)
- [Frequently Asked Questions (FAQ)](Frequently-Asked-Questions.md)
  - [How to configure Timezone](Frequently-Asked-Questions.md#how-to-configure-timezone)
  - [How to stop Dockupdater auto update](Frequently-Asked-Questions.md#how-to-stop-dockupdater-auto-update)
  - [How install Dockupdater without docker](Frequently-Asked-Questions.md#how-install-dockupdater-without-docker)
  - [How to remove container after service update](Frequently-Asked-Questions.md#how-to-remove-container-after-service-update)
  - [How to use with service but without stack](Frequently-Asked-Questions.md#how-to-use-with-service-but-without-stack)

## Overview

**Dockupdater** will monitor (all or specified by a label) running docker containers and running service (in docker swarm) and update them to the (latest or tagged) available image in the remote registry.

- Push your image to your registry and simply wait your defined interval for dockupdater to find the new image and redeploy your container autonomously.
- Notify you via many platforms courtesy of [Apprise](https://github.com/caronc/apprise) 
- Use with Docker swarm to update services on the latest available version
- Limit your server SSH access
- Useful to keep 3rd party container up-to-date

### Docker container

**Dockupdater** is deployed via docker image in a standalone container like so:

```bash
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater
```

> This is image is compatible for amd64, arm32, and arm64 CPU architectures

### Docker swarm (service)

**Dockupdater** can be deploy on a service like that:

```bash
version: "3.6"

services:
  dockupdater:
    image: dockupdater/dockupdater
    deploy:
      placement:
        constraints:
          - node.role == manager
```

> Dockupdater need to run on a manager node

## Getting helps

* [Issues list](https://github.com/dockupdater/dockupdater/issues)
* [Releases and changelogs](https://github.com/dockupdater/dockupdater/releases)
