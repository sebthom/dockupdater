If your running containers' docker images are stored in a secure registry that requires a username and password, simply run docupdater with 2 arguments or the equivalent environment variables.

### Command line arguments

```
docker run -d --name docupdater \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docupdater/docupdater --repo-user myUser --repo-pass myPassword
```

### Environment Variables

```
docker run -d --name docupdater \
  -e DOCUPDATER_REPO_USER=myUser -e DOCUPDATER_REPO_PASS=myPassword \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docupdater/docupdater
```

### Mount config.json (multiple registry credentials)

You can alternatively bind mount `~/.docker/config.json` which won't require the above environment variables and support authenticating to more than one docker registry in the event `REPO_USER` and `REPO_PASS` aren't the same for multiple sources.

```
docker run -d --name docupdater \
  -v $HOME/.docker/config.json:/root/.docker/config.json \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docupdater/docupdater
```