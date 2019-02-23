Command line arguments can be viewed by running:

```
docker run --rm docupdater/docupdater --help
```
> All command line arguments can be substituted with an environment variable. All examples will be given as environment variables for a `docker run -e option=option_value`.

***

* Usage
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
    * [Monitor](#monitor)
    * [Ignore](#ignore)
    * [Label](#label)
    * [Cleanup](#cleanup)
    * [Latest](#latest)
    * [Repository User](#repository-user)
    * [Repository Password](#repository-password)
  * [Notifications](#notifications)

***

### Help
**Type:** Boolean - Interrupting  
**Command Line:**  `-h, --help`  

Shows the help message then exits

### Version
**Type:** Boolean - Interrupting  
**Command Line:**  `-v, --version`  

Shows the current version number then exits

### Log Level
**Type:** String - Choice  
**Command Line:**  `-l, --log-level`  
**Environment Variable:** `DOCUPDATER_LOG_LEVEL`  
**Choices:**
* debug
* info
* warn
* error
* critical

**Default:** `info`  
**Example:** `-e DOCUPDATER_LOG_LEVEL=info`  

Sets your logging verbosity level.

## Scheduler
### Interval
**Type:** Integer  
**Command Line:**  `-i, --interval`  
**Environment Variable:** `DOCUPDATER_INTERVAL`
**Default**: `300`  
**Example:** `-e DOCUPDATER_INTERVAL=300`  

The interval in seconds between checking for updates. There is a hard-coded 30 second minimum. Anything lower than that will set to 30. 

### Cron
**Type:** String  
**Command Line:**  `-C, --cron`  
**Environment Variable:** `DOCUPDATER_CRON`  
**Default**: `None`  
**Example:** `-e DOCUPDATER_CRON="*/5 * * * *"`   

The schedule defined when to check for updates. If not defined, runs at interval.

### Run Once
**Type:** Boolean - Interrupting  
**Command Line:**  `-o, --run-once`  
**Environment Variable:** `DOCUPDATER_RUN_ONCE`  
**Default:** `False`  

Docupdater will only do a single pass of all container checks, and then exit. This is a great way to granularly control scheduling with an outside scheduler like cron. If during the single pass docupdater has to self-update, it will do another full pass after updating itself to ensure that all containers were checked.

## Docker Specifics
### Docker Socket
**Type:** String
**Command Line:**  `-d, --docker-socket`  
**Environment Variable:** `DOCUPDATER_DOCKER_SOCKETS`  
**Default:** `unix://var/run/docker.sock`  
**Example:** `-e DOCUPDATER_DOCKER_SOCKETS="unix://var/run/docker.sock"`  

Allows you to define the docker socket.

### Docker TLS
**Type:** Boolean  
**Command Line:**  `-t, --docker-tls`  
**Environment Variable:** `DOCUPDATER_DOCKER_TLS`  
**Default:** `False`  
**Example:** `-e DOCUPDATER_DOCKER_TLS=true -v $DOCKER_CERT_FOLDER:/root/.docker/`  

Enables docker TLS secure client connections by certificate

### Docker TLS Verify
**Type:** Boolean  
**Command Line:**  `-T, --docker-tls-verify`  
**Environment Variable:** `DOCUPDATER_DOCKER_TLS_VERIFY`  
**Default:** `True`  
**Example:** `-e DOCUPDATER_DOCKER_TLS_VERIFY=false`  

Verify CA certificate for docker deamon

### Label
**Type:** Boolean  
**Command Line:**  `-k, --label`  
**Environment Variable:** `DOCUPDATER_LABEL`  
**Default:** `False`  
**Example:** `-e DOCUPDATER_LABEL=true`  

This flag allows a more strict control over docupdater's updates. If the container or service does not have a `docupdater.enable` label, it will be ignored completely. See [Labels](Labels.md) for a list of all available labels.

### Cleanup
**Type:** Boolean  
**Command Line:**  `-c, --cleanup`  
**Environment Variable:** `DOCUPDATER_CLEANUP`  
**Default:** `False`  
**Example:** `-e DOCUPDATER_CLEANUP=true`  

Remove the old images after updating. If you have multiple containers using the same image, it will ensure all containers are updated before successfully removing the image.

### Latest
**Type:** Boolean  
**Command Line:**  `-L, --latest`  
**Environment Variable:** `DOCUPDATER_LATEST`  
**Default:** `False`  
**Example:** `-e DOCUPDATER_LATEST=true`  

Pull the `:latest` tags and update all containers to it, regardless of the current tag the container is running as. Can be override with the label `docupdater.latest`. See [Labels](Labels.md) for a list of all available labels.

### Repository User
**Type:** String  
**Command Line:**  `-r, --repo-user`  
**Environment Variable:** `DOCUPDATER_REPO_USER`  
**Default:** `None`  
**Example:** `-e DOCUPDATER_REPO_USER=johndoe1970`  

Define a username for repository authentication. Will be ignored without defining a repository password.

### Repository Password
**Type:** String  
**Command Line:**  `-R, --repo-pass`  
**Environment Variable:** `DOCUPDATER_REPO_PASS`  
**Default:** `None`  
**Example:** `-e DOCUPDATER_REPO_PASS=0791eodnhoj`  

Define a password for repository authentication. Will be ignored without defining a repository username.

## Notifications

**Type:** List - Space separated  
**Command Line:**  `-N, --notifiers`  
**Environment Variable:** `NOTIFIERS`  
**Default:** `None`  
**Example:** `-n NOTIFIERS="mailtos://myUsername:myPassword@gmail.com?to=receivingAddress@gmail.com jsons://webhook.site/something"`  

Docupdater uses [apprise](https://github.com/caronc/apprise) to support a large variety of notification platforms.

Notifications are sent per socket, per run. The notification contains the socket, the containers updated since last start, and a list of containers updated this pass with from/to SHA.

More information can be found in the [notifications docs](Notifications.md).
