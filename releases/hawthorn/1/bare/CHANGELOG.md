# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Fixed

- Fix build by installing py2neo 3.1.2 from its github repository
- Fix build after get-pip.py script moved location
- Fix pip install for python 2.7

## [hawthorn.1-3.3.0] - 2020-05-14

### Added

- Allow serving static files via a CDN

### Changed

- Collect static files in the `edxapp` image so it can run without mounting a volume
  for its static files in Kubernetes

## [hawthorn.1-3.2.0] - 2020-04-08

### Added

- Rate limiting authentication backend that works behind proxies

### Changed

- Refactor the way authentication backends are configured to make it straightforward
- Set basic authentification backend for development environment

### Fixed

- Remove hardcoded FILE_UPLOAD_STORAGE_BUCKET_NAME value to make sure it is configurable

## [hawthorn.1-3.1.1] - 2020-01-23

### Fixed

- Copy `webpack-stats.json` files to expected static files root path in case no
  static files volume is mounted

## [hawthorn.1-3.1.0] - 2020-01-15

### Changed

- Upgrade to a recent release of nodejs as the one packaged in Ubuntu was breaking the build

### Removed

- Checks that ensure required directories exist in volumes

## [hawthorn.1-3.0.0] - 2020-01-10

### Added

- Configure all cache backends
- Make Gunicorn timeout, workers and threads configurable via an environment
  variable

### Changed

- Move DATA_DIR to same location as for other flavors (breaking change)
- Make ORA2 configurable and use filesystem backend by default
- Stop inheriting from MKTG_URL_LINK_MAP default setting

### Fixed

- Ensure all required directories exists inside each volume
- Make Celery result backend configurable

## [hawthorn.1-2.8.0] - 2019-11-22

### Added

- Set replicaSet and read_preference in mongodb connection

## [hawthorn.1-2.7.1] - 2019-10-25

### Fixed

- Restore LOCALE_PATHS override for the LMS

## [hawthorn.1-2.7.0] - 2019-10-10

### Changed

- Add LOCALE_PATHS to configurable settings
- Remove useless timezone configuration
- Remove useless development dependencies

## [hawthorn.1-2.6.0] - 2019-02-08

### Added

- Make memcached host & port configurable.

## [hawthorn.1-2.5.1] - 2019-01-31

### Fixed

- Use default common setting for `TRACKING_IGNORE_URL_PATTERNS`

## [hawthorn.1-2.0.1] - 2018-10-02

### Fixed

- Add local node binaries to the path

## [hawthorn.1-2.0.0] - 2018-10-01

The development environment was not working properly since we upgraded to
`hawthorn` because assets are built differently in production and in
development. This release fixed the development environment and comes with a
complete rewrite of the `Dockerfile` to leverage multi-stage builds.

We identified a lot more improvements that could not be done because of design
issues in OpenEdx.

For example:

- get rid of the `node_modules` directory in the production image,
- avoid reinstalling everything after mounting sources as volumes in the
  development image.

We did not surrender on these improvements but will need to spend some time
demonstrating what is wrong to edX and submitting Pull Requests' to fix the
issues at their root.

### Changed

- Refactor the Dockerfile from scratch using multi-stage build

### Fixed

- Fixed development environment

## [hawthorn.1-1.0.6] - 2018-09-19

### Fixed

- Fix `EMAIL_BACKEND` default (follow-up of `766fcd8`, as `config` requires a
  `default` keyword)

## [hawthorn.1-1.0.5] - 2018-09-14

The database related settings (mysql & mongodb) were set in one big dictionary
variable containing all the parameters:

- some are secret like passwords and some aren't,
- some change at each deployment like host names and some never change.

In [Arnold](https://github.com/openfun/arnold), credentials are stored as
OpenShift secrets and injected as environment variables whereas non secret
settings are injected from a YAML file. For this reason, we needed to be able to
set each database setting separately.

### Added

- add `vim` editor to development container

### Changed

- set each database setting separately
- update the demo course to `hawthorn.1` to match the version of `edxapp` that we are running
- set a default configuration for password complexity so that automatic creation
  of users with `/auto_auth` works by default in development

### Fixed

- fix platform name and description default values to avoid de-serialization bug
  in OpenEdX while waiting for a fix on
  [edx-platform](https://github.com/edx/edx-platform)

## [hawthorn.1-1.0.4] - 2018-09-11

This debugging release is getting us closer to a functional `hawthorn.1` image
in [Arnold](https://github.com/openfun/arnold):

### Added

- Add missing setting for Celery default queues

### Changed

- Activate easy creation of test users in development
- Use LMS and CMS hosts as site names for the LMS and CMS respectively

### Fixed

- Fix bug on the configuration of the email backend in development
- Fix activating requirejs debugging mode in development

## [hawthorn.1-1.0.3] - 2018-09-11

### Added

This Release adds configuration formatters on all settings so that they can all
be set via environment variables. This is because environment variables can only
pass strings and some settings are expecting other types. Here are some examples
of formatters we use:

- Booleans: `bool`
- Integers: `int`
- Dictionaries or lists: `json.loads`
- Dates: `dateutil.parser.parse`

## [hawthorn.1-1.0.2] - 2018-09-10

### Added

- Add `mailcatcher` to handle the emails sent by `edxapp` in `fun-platform`
- Allow formatting settings passed as environment variables and apply it for
  `celery`, `mailcatcher` and the database configurations

### Changed

- Improve email settings to allow flexible configurations in each environment
- Deactivate `celery` to simplify development in `fun-platform`
- Move environment variables to environment files

### Fixed

- Fix `update_assets` in development `Dockerfile` to avoid the
  uninstalling/reinstalling that Open edX does by default.

## [hawthorn.1-1.0.1] - 2018-08-30

### Removed

Remove webpack stats from the statics target folder. There is no obvious reason
to store `webpack-stats.json` files in the `STATIC_ROOT` tree. It causes more
problems than it solves as we need to manually copy it during deployment since
it is not collected via `collectstatics`. Generating those files with
`update_assets` at the project root seems a reasonable choice.

## [hawthorn.1-1.0.0] - 2018-08-30

### Added

First experimental release of an `hawthorn.1` Docker image. This release is the
result of updating our OpenEdX images from `ginkgo` to `hawthorn.1`. It is not
functional and is intended for development and debugging work in
[Arnold](https://github.com/openfun/arnold).

[unreleased]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-3.3.0...HEAD
[hawthorn.1-3.3.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-3.2.0...hawthorn.1-3.3.0
[hawthorn.1-3.2.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-3.1.1...hawthorn.1-3.2.0
[hawthorn.1-3.1.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-3.1.0...hawthorn.1-3.1.1
[hawthorn.1-3.1.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-3.0.0...hawthorn.1-3.1.0
[hawthorn.1-3.0.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.8.0...hawthorn.1-3.0.0
[hawthorn.1-2.8.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.7.1...hawthorn.1-2.8.0
[hawthorn.1-2.7.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.7.0...hawthorn.1-2.7.1
[hawthorn.1-2.7.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.6.0...hawthorn.1-2.7.0
[hawthorn.1-2.6.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.5.1...hawthorn.1-2.6.0
[hawthorn.1-2.5.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.0.1...hawthorn.1-2.5.1
[hawthorn.1-2.0.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.0.0...hawthorn.1-2.0.1
[hawthorn.1-2.0.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.6...hawthorn.1-2.0.0
[hawthorn.1-1.0.6]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.5...hawthorn.1-1.0.6
[hawthorn.1-1.0.5]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.4...hawthorn.1-1.0.5
[hawthorn.1-1.0.4]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.3...hawthorn.1-1.0.4
[hawthorn.1-1.0.3]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.2...hawthorn.1-1.0.3
[hawthorn.1-1.0.2]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.1...hawthorn.1-1.0.2
[hawthorn.1-1.0.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-1.0.0...hawthorn.1-1.0.1
[hawthorn.1-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/hawthorn.1-1.0.0
