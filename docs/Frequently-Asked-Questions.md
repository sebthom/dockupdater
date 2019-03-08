# Frequently Asked Questions

* [How to configure Timezone](#how-to-configure-timezone)
* [How to stop Dockupdater auto update](#how-to-stop-dockupdater-auto-update)
* [How install Dockupdater without docker](#how-install-dockupdater-without-docker)
* [How to remove container after service update](#how-to-remove-container-after-service-update)

***

## How to configure Timezone

To more closely monitor dockupdater' actions and for accurate log ingestion, you can change the timezone of the container from UTC by setting the [`TZ`](http://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html) environment variable like so:

```bash
docker run -d --name dockupdater \
  -e TZ=America/Chicago \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater
```

## How to stop Dockupdater auto update

Your can add label `dockupdater.disable="true"` on the container or service to disable auto update.

If your run a standalone container for dockupdater:

```bash
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --label dockupdater.disable="true"
  dockupdater/dockupdater
```

If your run dockupdater with a stack:

```bash
version: "3.6"

services:
  dockupdater:
    image: dockupdater/dockupdater
    deploy:
      labels:
        dockupdater.disable: "true"
```

## How install Dockupdater without docker

dockupdater can also be installed via pip:

```bash
pip install dockupdater
```

And can then be invoked using the dockupdater command:

$ dockupdater --interval 300 --log-level debug

> Dockupdater need Python 3.6 or up

## How to remove containers after service update

By default Docker swarm keep 5 stop containers by service. You can configure that number at 0 to always remove old containers.

The update your docker swarm, run that command on a manager:

$ docker swarm update --task-history-limit=0
