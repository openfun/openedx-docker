# Open edX Docker

France Université Numérique introduces an alternative `Docker` approach to
install a complete and customized version of [Open edX](https://open.edx.org).

The idea is to handcraft a `Dockerfile`, in order to make the project simpler,
more flexible and fully operable by developers.

We hope this kind of `Docker` configuration can soon be included in the
edx-platform repository itself.

## Approach

This project builds a docker image that is ready for production.

At France Université Numérique, we are deploying Open edX Docker to OpenShift,
for many customers and in multiple environments using
[Arnold](https://github.com/openfun/arnold):

- The Open edX settings were polished to unlock powerful configuration
  management features: sensible defaults, flexible overrides using YAML files
  and/or environment variables, secure credentials using Ansible Vault and PGP
  keys,
- We focused on a best practice installation of `edxapp`, the core Open edX
  application. You can build you own image by adding specific Xblocks or Django
  apps in a `Dockerfile` inheriting from this one (see
  <https://github.com/openfun/fonzie> for an example).

Docker compose is only used for development purposes so that we can code locally
and see our changes immediately:

- sources and configuration files are mounted from the host,
- the Docker CMD launches Django's development server instead of `gunicorn`,
- ports are opened on the application containers to allow bypassing `nginx`.

Docker compose also allows us to run a complete project in development,
including database services which in production are not run on Docker. See the
[docker-compose file](./docker-compose.yml) for details on each service:

- **mysql:** the SQL database used to structure and persist the application
  data,
- **mongodb:** the no-SQL database used to store course content,
- **memcached:** the cache engine,
- **lms:** the Django web application used by learners,
- **cms:** the Django web application used by teachers,
- **forum:** the Ruby web application serving the discussion forum, **TODO**
- **ecommerce:** the Django web application used for payments, **TODO**
- **xqueue:** the interface for the LMS to communicate with external grader
  services, **TODO**
- **nginx:** the front end web server configured to serve static/media files and
  proxy other requests to Django.

## Alternative projects

If what you're looking for is a quick 1-click installation of the complete
Open edX stack, you may take a look at Régis Behmo's work
[here](https://github.com/regisb/openedx-docker).

## Getting started

Make sure you have a recent version of [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install) installed on your laptop:

    $ docker -v
      Docker version 17.12.0-ce, build c97c6d6

    $ docker-compose --version
      docker-compose version 1.17.1, build 6d101fb

⚠️ `Docker Compose` version 1.19 is not supported because of a bug (see
https://github.com/docker/compose/issues/5686). Please downgrade to 1.18 or
upgrade to a higher version.

Start the full project by running:

```bash
$ make bootstrap
```

You should now be able to view the web applications:

- LMS served by nginx at: [http://localhost:8073](http://localhost:8073)
- CMS served by nginx at: [http://localhost:8083](http://localhost:8083)

See other available commands by running:

```bash
$ make --help
```

## Developer guide

If you intend to work on edx-platform or its configuration, you'll first need to
clone the git repository locally and compile static files in local directories
that are mounted as docker volumes in the target container:

```bash
$ make clone
$ make dev-assets
```

**Tip:** you will need to update assets at every new `edx-platform` checkout.

Now you can start services development server _via_:

```bash
$ make dev
```

You should be able to view the web applications:

- LMS served by runserver at: [http://localhost:8072](http://localhost:8072)
- CMS served by runserver at: [http://localhost:8082](http://localhost:8082)

### Hacking with themes

To work on a particular theme, we invite you to use the `paver watch_assets`
command; _e.g._:

```bash
$ make dev-watch
```

**Troubleshooting**: if the command above raises the following error:

```
OSError: inotify watch limit reached
```

Then you will need to increase the **host**'s `fs.inotify.max_user_watches` kernel
setting (for reference, see https://unix.stackexchange.com/a/13757):

```conf
# /etc/sysctl.conf (debian based)
fs.inotify.max_user_watches=524288
```

# Docker images

The plan is to prepare several flavors of images, the docker files and settings
of which are living in their own branch (e.g. ginkgo.1, eucalyptus-funwb,
dogwood-funmooc,...)

Branch names on the current repository are of the form:
**{edx-version}[-{fork-name}]** Two words separated by a dash, the second word
being optional:

- **edx-version:** name of the upstream `edx-platform` version (e.g. ginkgo.1),
- **fork-name:** name of the specific project fork, if any (e.g. funwb).

We are pushing to `DockerHub` only images that are the result of a tag
respecting the pattern: **{branch-name}-x.y.z**

Here are some valid examples:

- dogwood.3-1.0.3
- dogwood.2-funmooc-17.6.1
- eucalyptus-funwb-2.3.19

Each time we push to `DockerHub` the new version of an image, we also update the
`latest` version so that our `latest` images are always up-to-date:

- eucalyptus-funwb-2.3.19 -> eucalyptus-funwb-latest
- eucalyptus-funwb-2.3.19-dev -> eucalyptus-funwb-latest-dev

## License

The code in this repository is licensed under the GNU AGPL-3.0 terms unless
otherwise noted.

Please see `LICENSE` for details.
