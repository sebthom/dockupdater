# Options usage

Command line arguments can be viewed by running:

```bash
docker run --rm dockupdater/dockupdater --help
```

All command line arguments can be substituted with an environment variable. All examples will be given as environment variables for a `docker run -e option=option_value`.

On a stack file (Docker swarm), you may set the environment variable like so:

```bash
version: "3.6"

services:
  dockupdater:
    image: dockupdater/dockupdater
    environment:
        - INTERVAL=30
        - LABEL=true
    deploy:
      labels:
        dockupdater.disable: "true"
      placement:
        constraints:
          - node.role == manager
```

> On stack mode, environment variables should not be enclosed in quotation marks.

***

* [Help](#help)
* [Version](#version)
* [Log Level](#log-level)
* [Scheduler](#scheduler)
  * [Interval](#interval)
  * [Cron](#cron)
  * [Run Once](#run-once)
* [Docker Specifics](#docker-specifics)
  * [Docker Sockets](#docker-sockets)
  * [Docker TLS Verify](#docker-tls-verify)
  * [Label](#label)
  * [Disable containers check](#disable-containers-check)
  * [Disable services check (swarm)](#disable-services-check-swarm)
  * [Cleanup](#cleanup)
  * [Latest](#latest)
  * [Repository User](#repository-user)
  * [Repository Password](#repository-password)
  * [Wait time](#wait-time)
  * [Recreate first](#recreate-first)
* [Notifications](#notifications)
  * [Notifiers](#notifiers)
  * [Template file](#template-file)
  * [Skip start notification](#skip-start-notification)

***

### Help

**Type:** `Boolean - Interrupting`  
**Command Line:**  `-h, --help`  

Shows the help message then exits.

### Version

**Type:** `Boolean - Interrupting`
**Command Line:**  `-v, --version`  

Shows the current version number then exits

### Log Level

**Type:** `String - Choice`  
**Command Line:**  `-l, --log-level`  
**Environment Variable:** `LOG_LEVEL`  
**Choices:**

* debug
* info
* warn
* error
* critical

**Default:** `info`  
**Example:** `-e LOG_LEVEL=info`  

Sets your logging verbosity level.

## Scheduler

### Interval

**Type:** `Integer`  
**Command Line:**  `-i, --interval`  
**Environment Variable:** `INTERVAL`
**Default**: `300`  
**Example:** `-e INTERVAL=300`  

The interval in seconds between checking for updates. There is a hard-coded 30 second minimum. Anything lower than that will set to 30. 

### Cron

**Type:** `String`  
**Command Line:**  `-C, --cron`  
**Environment Variable:** `CRON`  
**Default**: `None`  
**Example:** `-e CRON="*/5 * * * *"`   

The schedule defined when to check for updates. If not defined, runs at interval.

### Run Once

**Type:** `Boolean - Interrupting`  
**Command Line:**  `-o, --run-once`  
**Environment Variable:** `RUN_ONCE`  
**Default:** `False`  

Dockupdater will only do a single pass of all container checks, and then exit. This is a great way to granularly control scheduling with an outside scheduler like cron. If during the single pass dockupdater has to self-update, it will do another full pass after updating itself to ensure that all containers were checked.

## Docker Specifics

### Docker Socket

**Type:** `List - Space separated`
**Command Line:**  `-d, --docker-sockets`  
**Environment Variable:** `DOCKER_SOCKETS`  
**Default:** `unix://var/run/docker.sock`  
**Availability:** `containers` `services`  
**Example:** `-e DOCKER_SOCKETS="unix://var/run/docker.sock tcp://192.168.1.100:2376"`  

Allows you to define the docker socket.

### Docker TLS

**Type:** `Boolean`  
**Command Line:**  `-t, --docker-tls`  
**Environment Variable:** `DOCKER_TLS`  
**Default:** `False`  
**Availability:** `containers` `services`  
**Example:** `-e DOCKER_TLS=true -v $DOCKER_CERT_FOLDER:/root/.docker/`  

Enables docker TLS secure client connections by certificate

### Docker TLS Verify

**Type:** `Boolean`  
**Command Line:**  `-T, --docker-tls-verify`  
**Environment Variable:** `DOCKER_TLS_VERIFY`  
**Default:** `True`  
**Availability:** `containers` `services`  
**Example:** `-e DOCKER_TLS_VERIFY=false`  

Verify CA certificate for docker deamon

### Label

**Type:** `Boolean`  
**Command Line:**  `-k, --label`  
**Environment Variable:** `LABEL`  
**Default:** `False`  
**Availability:** `containers` `services`  
**Example:** `-e LABEL=true`  

This flag allows a more strict control over Dockupdater's updates. If the container or service does not have a `dockupdater.enable` label, it will be ignored completely.

### Disable services check (swarm)

**Type:** `Boolean`  
**Command Line:**  `--disable-services-check`  
**Environment Variable:** `DISABLE_SERVICES_CHECK`  
**Default:** `False`  
**Availability:** `services`  
**Example:** `-e DISABLE_SERVICES_CHECK=true`  

Disable the scan for services (swarm). With this flag only standalone container will be updated.

### Disable containers check

**Type:** `Boolean`  
**Command Line:**  `--disable-containers-check`  
**Environment Variable:** `DISABLE_CONTAINERS_CHECK`  
**Default:** `False`  
**Availability:** `containers`  
**Example:** `-e DISABLE_CONTAINERS_CHECK=true`  

Disable the scan for standalone containers.

### Cleanup

**Type:** `Boolean`  
**Command Line:**  `-c, --cleanup`  
**Environment Variable:** `CLEANUP`  
**Default:** `False`  
**Availability:** `containers`  
**Override label:** [`dockupdater.cleamup`](Labels.md#cleanup)
**Example:** `-e CLEANUP=true`  

Remove the old images after updating. If you have multiple containers using the same image, it will ensure all containers are updated before successfully removing the image.

### Latest

**Type:** `Boolean`  
**Command Line:**  `-L, --latest`  
**Environment Variable:** `LATEST`  
**Default:** `False`  
**Availability:** `containers` `services`  
**Override label:** [`dockupdater.latest`](Labels.md#latest)
**Example:** `-e LATEST=true`  

Pull the `:latest` tags and update all containers to it, regardless of the current tag the container is running as.

### Repository User

**Type:** `String`  
**Command Line:**  `-r, --repo-user`  
**Environment Variable:** `REPO_USER`  
**Default:** `None`  
**Availability:** `containers` `services`  
**Example:** `-e REPO_USER=johndoe1970`  

Define a username for repository authentication. Will be ignored without defining a repository password.

### Repository Password

**Type:** `String`  
**Command Line:**  `-R, --repo-pass`  
**Environment Variable:** `REPO_PASS`  
**Default:** `None`  
**Availability:** `containers` `services`  
**Example:** `-e REPO_PASS=0791eodnhoj`  

Define a password for repository authentication. Will be ignored without defining a repository username.

### Stop signal

**Type:** `Integer`  
**Command Line:**  `--stop-signal`  
**Environment Variable:** `STOP_SIGNAL`  
**Default:** `None`  
**Availability:** `containers`  
**Override label:** [`dockupdater.stop_signal`](Labels.md#stop_signal)
**Example:** `-e STOP_SIGNAL=12`  

Define a stop signal to send to the container instead of SIGKILL. Default behavior is to use default docker stop command.

### Wait time

**Type:** `Integer`  
**Command Line:**  `-w, --wait`  
**Environment Variable:** `WAIT`  
**Default:** `0`  
**Availability:** `containers` `services`  
**Override label:** [`dockupdater.wait`](Labels.md#wait-time)
**Example:** `-e WAIT=60`  

Define a time in seconds to wait after an update before updating any others containers or services.

### Recreate first

**Type:** `Integer`  
**Command Line:**  `-F, --recreate-first`  
**Environment Variable:** `RECREATE_FIRST`  
**Default:** `0`  
**Availability:** `containers`  
**Override label:** [`dockupdater.recreate_first`](Labels.md#recreate-first)
**Example:** `-e RECREATE_FIRST=true`  

Work only with standalone container. To minimize application down time, we could create the new container before deleting the old.

Warning: This feature doesn't work if you have exposed ports. We highly recommend to use a load balancer like [Traefik](https://traefik.io/) if you need to use exposed ports with dockupdater.

Self update of dockupdater always use this feature.

## Notifications

### Notifiers

**Type:** `List - Space separated`  
**Command Line:**  `-N, --notifiers`  
**Environment Variable:** `NOTIFIERS`  
**Default:** `None`  
**Override label:** [`dockupdater.notifiers`](Labels.md#notifiers)
**Example:** `-e NOTIFIERS="mailtos://myUsername:myPassword@gmail.com?to=receivingAddress@gmail.com jsons://webhook.site/something"`  

Dockupdater uses [apprise](https://github.com/caronc/apprise) to support a large variety of notification platforms.

Notifications are sent for every update. The notification contains the container/service updated.

More information can be found in the [notifications docs](Notifications.md).

### Template file

**Type:** `Path`  
**Command Line:**  `--template-file`  
**Environment Variable:** `TEMPLATE_FILE`  
**Default:** `None`  
**Override label:** [`dockupdater.template_file`](Labels.md#template-file)
**Example:** `-e TEMPLATE_FILE="/template.j2"`  

Use this template instead of default template file. We use jinja2 template style to parse the template. Must be a valid path, don't forget to mount the template in the container.

See this example of template file:
```
{{ object.name }} ({{ object.get_image_name() }}:{{ object.get_tag() }}) updated from {{ object.get_current_id() }} to {{ object.get_latest_id() }}
```

### Skip start notification

**Type:**  `Boolean`
**Command Line:**  `--skip-start-notif`  
**Environment Variable:** `SKIP_START_NOTIF`  
**Default:** `False`  
**Example:** `-e SKIP_START_NOTIF=true`  

Dockupdater send a notification when it start. That option disable this notification.

***

Next: [Customize usage with labels](Labels.md)
