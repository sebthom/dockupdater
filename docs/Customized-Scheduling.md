# Scheduling

## Interval
Docupdater by default use the `--interval` [option](Options.md) to run task every X seconds.

## Cron
Docupdater can by use with [cron](https://crontab.guru/) to customize schedule of your task.

Example using Docupdater to update containers every Monday at 5AM:

**Docker**

```bash
docker run --rm -d --name docupdater -v /var/run/docker.sock:/var/run/docker.sock docupdater/docupdater --cron 0 5 * * 1
```
