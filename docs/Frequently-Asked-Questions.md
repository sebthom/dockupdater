# Frequently Asked Questions

* [How to configure Timezone](#how-to-configure-timezone)
* [How to stop Docupdater auto update](#how-to-stop-docupdater-auto-update)
* [How install Docupdater without docker](#how-install-docupdater-without-docker)
* [How to remove container after service update](#how-to-remove-container-after-service-update)

***

## How to configure Timezone

To more closely monitor docupdater' actions and for accurate log ingestion, you can change the timezone of the container from UTC by setting the [`TZ`](http://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html) environment variable like so:

```bash
docker run -d --name docupdater \
  -e TZ=America/Chicago \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docupdater/docupdater
```

## How to stop Docupdater auto update

Your can add label `docupdater.disable="true"` on the container or service to disable auto update.

If your run a standalone container for docupdater:

```bash
docker run -d --name docupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --label docupdater.disable="true"
  docupdater/docupdater
```

If your run docupdater with a stack:

```bash
version: "3.6"

services:
  docupdater:
    image: docupdater/docupdater
    deploy:
      labels:
        docupdater.disable: "true"
```

## How install Docupdater without docker

docupdater can also be installed via pip:

```bash
pip install docupdater
```

And can then be invoked using the docupdater command:

$ docupdater --interval 300 --log-level debug

> Docupdater need Python 3.6 or up

## How to remove containers after service update

By default Docker swarm keep 5 stop containers by service. You can configure that number at 0 to always remove old containers.

The update your docker swarm, run that command on a manager:

$ docker swarm update --task-history-limit=0
