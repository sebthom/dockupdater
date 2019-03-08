# Customized Scheduling

## Interval

Dockupdater by default use the `--interval` [option](Options.md) to run task every X seconds.

## Cron

Dockupdater can by use with [cron](https://crontab.guru/) to customize schedule of your task.

Example using Dockupdater to update containers every Monday at 5AM:

**Docker**

```bash
docker run --rm -d --name dockupdater -v /var/run/docker.sock:/var/run/docker.sock dockupdater/dockupdater --cron 0 5 * * 1
```

***

Next: [Notifications](Notifications.md)
