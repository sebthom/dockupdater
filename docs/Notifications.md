# Notifications

Dockupdater uses [apprise](https://github.com/caronc/apprise) to support a large variety of notification platforms.

***

* [Sample integrations](#sample-integration)
  * [Email](#email)
  * [Webhooks](#webhooks)
  * [Slack](#slack)
* [More integration](#more-integrations)
* [Startup notifications](#startup-notifications)
* [Multiple notifications channels](#multiple-notifications-channels)
* [Override notifications with labels](#override-notifications-with-labels)

***

## Sample integrations

### Email

```shell
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater -N 'mailtos://myUsername:myPassword@gmail.com?to=receivingAddress@gmail.com'
```

### Webhooks

```shell
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater -N 'jsons://webhook.site/something'
```

### Slack

```shell
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater -N 'slack://botName@TOKEN1/TOKEN2/TOKEN3/#mychannel'
```

## More integrations

See all notification integrations [supported by apprise](https://github.com/caronc/apprise#supported-notifications)

## Startup notifications

By default, if notifications are enabled, all notification platforms will be fired with a body stating that dockupdater has started with the current time set in the container and the timestamp of when dockupdater will next check for updates. We can disable this bahevior with option [--skip-start-notif](Options.md#skip-start-notifation).

## Multiple notifications channels

You can specify multiple notifications by separate each with a space. Example, to send 3 notifications:

```shell
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater -N 'jsons://webhook.site/something jsons://webhook.site/otherthing slack://TOKEN1/TOKEN2/TOKEN3/#devops'
```

## Override notifications with labels

Here a complete example of docker swarm with multiple notifications and multiple overrides.

```bash
version: "3.6"

configs:
  dockupdater-template:
    file: template.j2

services:
  dockupdater:
    image: dockupdater/dockupdater
    environment:
      NOTIFIERS: "slack://${SLACK_TOKEN}/#devops-monitoring"
      TZ: "America/Montreal"
      TEMPLATE_FILE: "/template.j2"
    configs:
      - source: dockupdater-template
        target: /template.j2
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    deploy:
      placement:
        constraints:
          - node.role == manager

  testA:
    image: myorg/testimage

  testB:
    image: myorg/testimage
    deploy:
      labels:
        dockupdater.notifiers: "slack://${SLACK_TOKEN}/#devops-monitoring slack://${SLACK_TOKEN}/#teamB"

  testC:
    image: myorg/testimage
    deploy:
      labels:
        dockupdater.notifiers: ""
```

With the template file `template.j2`:

```
{% raw %}{{ object.name }} ({{ object.get_image_name() }}: {{ object.get_tag() }}){% endraw %}
```


On this example:

* testA will send update notifications on `#devops-monitoring` channel.
* testB will send update notifications on `#devops-monitoring` and `#teamB` channel.
* testC will not send update notifications.

***

Next: [Frequently Asked Questions (FAQ)](Frequently-Asked-Questions.md)
