# Private registries

If your running docker images stored in a secure registry that requires a username and password, simply run dockupdater with 2 arguments or the equivalent environment variables.

## Command line arguments

```
docker run -d --name dockupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater --repo-user myUser --repo-pass myPassword
```

## Environment Variables

```
docker run -d --name dockupdater \
  -e REPO_USER=myUser -e REPO_PASS=myPassword \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater
```

## Mount config.json (multiple registry credentials)

You can alternatively bind mount `~/.docker/config.json` which won't require the above environment variables and support authenticating to more than one docker registry in the event `REPO_USER` and `REPO_PASS` aren't the same for multiple sources.

```
docker run -d --name dockupdater \
  -v $HOME/.docker/config.json:/root/.docker/config.json \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dockupdater/dockupdater
```

***

Next: [Customized Scheduling](Customized-Scheduling.md)
