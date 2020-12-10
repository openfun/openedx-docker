# Open edX Docker

France Université Numérique introduces an alternative `Docker` approach to
install a complete and customized version of [Open edX](https://open.edx.org).

The idea is to handcraft a `Dockerfile`, in order to make the project simpler,
more flexible and fully operable by developers.

## Quick preview

If you're looking for a quick preview of OpenEdX Docker, you can take a look
at our dedicated [demo site](https://demo.richie.education).

It is connected back-to-back with a demo of Richie,
[a CMS for Open Education](https://richie.education) based on Django.

Two users are available for testing:

- admin: `admin@example.com`/`admin`
- student: `edx@example.com`/`edx`

Richie's admin is available at https://demo.richie.education/admin/ and can be
accessed via the following user account: `admin`/`admin`.

The demonstration databases are regularly flushed.

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
  https://github.com/openfun/fonzie for an example).

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
- **nginx:** the front end web server configured to serve static/media files and
  proxy other requests to Django.
- **mailcatcher** the email backend

Concerning Redis, it is possible to run a single redis instance (the default choice)
or to run redis with sentinel to simulate a HA instance.
To use Redis sentinel you have to set the `REDIS_SERVICE` environment variable
to `redis-sentinel`:

```bash
$ export REDIS_SERVICE=redis-sentinel
```

To switch back to the single redis instance, unset this environment variable:

```bash
$ unset REDIS_SERVICE
```

## Prerequisite

Make sure you have a recent version of [Docker](https://docs.docker.com/install)
and [Docker Compose](https://docs.docker.com/compose/install) installed on your
laptop:

```bash
$ docker -v
  Docker version 17.12.0-ce, build c97c6d6

$ docker-compose --version
  docker-compose version 1.17.1, build 6d101fb
```

⚠️ `Docker Compose` version 1.19 is not supported because of a bug (see
https://github.com/docker/compose/issues/5686). Please downgrade to 1.18 or
upgrade to a higher version.

## Getting started

First, you need to choose a release/flavor of OpenEdx versions we support. You
can list them and get instructions about how to select/activate a target release
using the `bin/activate` script. An example output follows:

```bash
$ bin/activate
Select an available release to activate:
[1] master/0/bare (default)
[2] hawthorn/1/bare
[3] hawthorn/1/oee
Your choice: 3

# Copy/paste hawthorn/1/oee environment:
export EDX_RELEASE="hawthorn.1"
export FLAVOR="oee"
export EDX_RELEASE_REF="open-release/hawthorn.1"
export EDX_DEMO_RELEASE_REF="open-release/hawthorn.1"

# Or run the following command:
. ${HOME}/Work/openedx-docker/releases/hawthorn/1/oee/activate

# Check your environment with:
make info
```

Once your environment is set, start the full project by running:

```bash
$ make bootstrap
```

You should now be able to view the web applications:

- LMS served by `nginx` at: [http://localhost:8073](http://localhost:8073)
- CMS served by `nginx` at: [http://localhost:8083](http://localhost:8083)

See other available commands by running:

```bash
$ make --help
```

## Developer guide

If you intend to work on edx-platform or its configuration, you'll need to
compile static files in local directories that are mounted as docker volumes in
the target container:

```bash
$ make dev-assets
```

Now you can start services development server _via_:

```bash
$ make dev
```

You should be able to view the web applications:

- LMS served by Django's development server at:
  [http://localhost:8072](http://localhost:8072)
- CMS served by Django's development server at:
  [http://localhost:8082](http://localhost:8082)

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

Then you will need to increase the **host**'s `fs.inotify.max_user_watches`
kernel setting (for reference, see https://unix.stackexchange.com/a/13757):

```ini
# /etc/sysctl.conf (debian based)
fs.inotify.max_user_watches=524288
```

## Available Docker images

The aim of this project is to prepare several flavors of images, the docker
files and settings of which are living in their own directory (see
[`releases/`](./releases/))

Release paths on the current repository are of the form:

```
{release name}/{release number}/{flavor}
```

With:

- **release name**: OpenEdx release name (_e.g._ `hawthorn`)
- **release number**: OpenEdx release number (_e.g._ `1`)
- **flavor**: the release flavor (_e.g._ `bare` for standard OpenEdx release and
  `oee` for OpenEdx Extended release).

We are pushing to `DockerHub` only images that are the result of a tag
respecting the following pattern:

```
{release}(-{flavor})-x.y.z
```

The `release` (_e.g._ `hawthorn.1`) typically includes the `release name`
(_e.g._ `hawthorn`) and the `release number` (_e.g._ `1`). The flavor is
optional.

Here are some valid examples:

- `dogwood.3-1.0.3`
- `hawthorn.1-oee-2.0.1`

## Nginx

This project also provides an nginx companion image that can be used
alongside the `edxapp` image for faster deployments and better performance.

The classical way to handle and serve static files in a Django application is
to collect them (using the `collectstatic` management command) and post-process
them using an appropriate storage back-end that uses cache-busting techniques
to avoid old _versus_ new static files collisions (_e.g._
`ManifestStaticFilesStorage`).

Depending on the `edx-platform` release, some files may not benefit from a
cache busting md5 hash, leading to unexpected side effects during deployment.

To prevent such behavior, for each new `openedx-docker` release, we will also
release an
[`edxapp-nginx`](https://hub.docker.com/repository/docker/fundocker/edxapp-nginx/)
image with the same Docker tag. This image is an [OpenShift-ready `nginx`
image](https://github.com/openfun/openshift-docker#nginx) with embedded
`edxapp`'s static files. You are supposed to use this image to serve your
static files, media and reverse proxy to the version-matching `edxapp` instance.

## Alternative projects

If what you're looking for is a quick 1-click installation of the complete Open
edX stack, you may take a look at [Tutor](https://github.com/overhangio/tutor).

## License

The code in this repository is licensed under the GNU AGPL-3.0 terms unless
otherwise noted.

Please see [`LICENSE`](./LICENSE) for details.
