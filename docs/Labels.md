# Customize usage with labels

Label on container or service can override the default behavior.

You can use the LABEL instruction on the Dockerfile or add label on the run command: `docker run -it -d --label docupdater.disable=true docupdater/docupdater`.

See this example of stack file to add a label on a service (Docker swarm):

```bash
version: "3.6"

services:
  docupdater:
    image: docupdater/docupdater
    deploy:
      labels:
        docupdater.disable: "true"
      placement:
        constraints:
          - node.role == manager
```

***

* [Disable update](#disable-update)
* [Enable update](#enable-update)
* [Latest](#latest)
* [Stop signal](#stop-signal)
* [Wait time](#wait-time)
* [Recreate first](#recreate-first)
* [Notifiers](#notifiers)
* [Template file](#template-file)

***

### Disable update

**Label:** `docupdater.disable`  
**Availability:** `containers` `services`  
**Example:** `docupdater.disable: "true"`  

Disable update for the service or container.

### Enable update

**Label:** `docupdater.enable`  
**Availability:** `containers` `services`  
**Example:** `docupdater.enable: "true"`  

When docupdater is start with option [--label](Options.md#Label), this label enable update for container or service.

### Latest

**Label:** `docupdater.latest`  
**Availability:** `containers` `services`  
**Equivalent option:** [`--latests`](Options.md#latest)  
**Example:** `docupdater.latest: "true"`  

With this label, the container or service will always pull the latest tag.

### Stop signal

**Label:** `docupdater.stop_signal`  
**Availability:** `containers`  
**Equivalent option:** [`--stop-signal`](Options.md#stop-signal)  
**Example:** `docupdater.stop_signal: 1`  

Define a stop signal to send to the container instead of SIGKILL. Can be string or int.

### Wait time

**Label:** `docupdater.wait`  
**Availability:** `containers` `services`  
**Equivalent option:** [`--wait`](Options.md#wait-time)  
**Example:** `docupdater.wait: 60`  

Define a time in seconds to wait after an update before updating any others containers or services.

### Recreate first

**Label:** `docupdater.recreate_first`  
**Availability:** `containers`  
**Equivalent option:** [`--recreate-first`](Options.md#recreate-first)  
**Example:** `docupdater.recreate_first: "true"`  

To minimize application down time, we could create the new container before deleting the old. See complete documentations on [options docs](Options.md#recreate-first).

### Notifiers

**Label:** `docupdater.notifiers`  
**Availability:** `containers` `services`  
**Equivalent option:** [`--notifiers`](Options.md#notifiers)  
**Example:** `docupdater.notifiers: ""`  

This override the default notifiers. You can disable notification for a specific container or service to set the label to an empty value (like the example). See the [notifications documentation](Notifications.md).

### Template file

**Label:** `docupdater.template_file`  
**Availability:** `containers` `services`  
**Equivalent option:** [`--template-file`](Options.md#template-file)  
**Example:** `docupdater.template_file: "/template.j2"`  

That override for this container or service the notification message to use. See [notifications docs](Notifications.md) for example.

***

Next: [Private Registries](Private-Registries.md)
