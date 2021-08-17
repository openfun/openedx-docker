# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

## [eucalyptus.3-wb-1.10.0] - 2021-08-17

### Changed

- Upgrade `fun-apps` to 2.5.0+wb for protection against VideoFront downtimes

### Fixed

- Fix build after get-pip.py script moved location

## [eucalyptus.3-wb-1.9.4] - 2021-02-11

### Fixed

- Upgrade to xblock-proctor-exam to 1.0.0 to fix proctoring after API change
- Fix pip install for python 2.7

## [eucalyptus.3-wb-1.9.3] - 2020-09-08

### Fixed

- Pin django-classy-tags to 0.8.0 to avoid breaking changes

## [eucalyptus.3-wb-1.9.2] - 2020-09-01

### Fixed

- Pin `django-redis` version to `4.5.0` to be able to use
  `django-redis-sentinel-redux`.
- Adjust settings to support `REDIS_SERVICE=redis-sentinel`

## [eucalyptus.3-wb-1.9.1] - 2020-07-20

### Changed

- Upgrade `fun-apps` to 2.4.2+wb

## [eucalyptus.3-wb-1.9.0] - 2020-05-14

### Added

- Allow serving static files via a CDN
- Add `django-redis-sentinel-redux` to allow the use of Redis Sentinel for
  Django cache

### Changed

- Collect static files in the `edxapp` image so it can run without mounting a
  volume for its static files in Kubernetes
- Configure most Django cache backends to Redis

### Removed

- Remove now useless Memcached settings

## [eucalyptus.3-wb-1.8.1] - 2020-04-17

### Changed

- Set basic authentification backend for development environment
- Upgrade `fun-apps` to `2.4.1+wb` to fix email report recipient bug

## [eucalyptus.3-wb-1.8.0] - 2020-04-03

### Added

- Rate limiting authentication backend that works behind proxies

### Changed

- Refactor the way authentication backends are configured to make it
  straightforward
- Upgrade `fun-apps` to `2.4.0+wb` to get rewritten management command to change
  course enrollments from `audit` to `honor`. This command will be used by a
  cron job.

## [eucalyptus.3-wb-1.7.4] - 2020-03-24

### Changed

- Upgraded `libcast-xblock` to 0.6.1

## [eucalyptus.3-wb-1.7.3] - 2020-03-13

### Fixed

- Fix setting `AUTHENTICATION_BACKENDS` to allow activating third party authentication

## [eucalyptus.3-wb-1.7.2] - 2020-02-19

### Fixed

- Add missing settings related to bokecc video provider backend in LMS config

## [eucalyptus.3-wb-1.7.1] - 2020-02-18

### Fixed

- Add missing settings related to bokecc video provider backend

## [eucalyptus.3-wb-1.7.0] - 2020-02-17

### Added

- Upgrade fun-apps to `2.3.1+wb` to add bokecc video provider backend

### Fixed

- Remove hardcoded FILE_UPLOAD_STORAGE_BUCKET_NAME value to make sure it is configurable

## [eucalyptus.3-wb-1.6.3] - 2020-01-23

### Fixed

- Upgrade `fun-apps` to `2.2.1+wb`

## [eucalyptus.3-wb-1.6.2] - 2020-01-22

### Changed

- Edx-platform fork git reference recently moved to `eucalyptus.3-wb`

## [eucalyptus.3-wb-1.6.1] - 2020-01-11

### Removed

- Checks that ensure required directories exist in volumes

## [eucalyptus.3-wb-1.6.0] - 2020-01-10

### Added

- Make Gunicorn workers and threads configurable via an environment variable

### Fixed

- Neutralize thumbnails creation as `eucalyptus.3-wb` is not using them
- Ensure all required directories exist inside each volume

### Removed

- Alternate queues settings to extend CELERY_QUEUES for cross-process workers

## [eucalyptus.3-wb-1.5.0] - 2020-01-08

### Changed

- Upgrade fun-apps to 2.2.0+wb
- Make ORA2 configurable and use filesystem backend by default

### Fixed

- Configure all cache backends as they are in FUN's production instance
- Add missing `fun` application templates directory to default templates directories
  to activate `videoupload` templates

## [eucalyptus.3-wb-1.4.0] - 2020-01-03

### Changed

- Stop inheriting from MKTG_URL_LINK_MAP default setting
- Relocate FUN certificates to media files instead of specific volume
- Refactor FUN settings as fine tuning that comes after the main settings

## [eucalyptus.3-wb-1.3.1] - 2019-12-27

### Fixed

- Refactor settings to repair and clean what is cms versus lms, edx versus
  fun-apps, configurable versus defined by code.

## [eucalyptus.3-wb-1.3.0] - 2019-12-26

### Added

- Make Gunicorn timeout configurable via an environment variable

## [eucalyptus.3-wb-1.2.2] - 2019-12-26

### Fixed

- Allow configuring the configurable LTI consumer xblock

### Security

- Remove selftest from installed apps to stop exposing settings on a url

## [eucalyptus.3-wb-1.2.1] - 2019-12-24

### Fixed

- `AUTH_TOKENS` was wrongly used as a dictionary and default values were lost

## [eucalyptus.3-wb-1.2.0] - 2019-12-20

### Added

- Force edX to use `libcast_xblock` as default video xblock
- Use custom demo course for FUN's flavors

### Fixed

- Add missing setting `LMS_ROOT_URL` used to compute absolute urls
- Fix `GITHUB_REPO_ROOT` and `DATA_DIR` settings

## [eucalyptus.3-wb-1.1.0] - 2019-12-18

### Changed

- Upgrade to nodejs 10 engine

### Fixed

- Rolled back default static files storage backend

## [eucalyptus.3-wb-1.0.5] - 2019-12-16

### Fixed

- Properly configure locales
- Remove duplicated `redis` package installation
- Configure `general` cache backend including cache keys sanitizing function
- Fix broken CMS JS build by enabling Pipeline's static files storage

## [eucalyptus.3-wb-1.0.4] - 2019-12-12

### Changed

- Declare redis as the default session engine

## [eucalyptus.3-wb-1.0.3] - 2019-12-10

### Fixed

- Fix redis release compatibility with celery-redis-sentinel (_e.g._ redis
  2.x.x)

## [eucalyptus.3-wb-1.0.2] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [eucalyptus.3-wb-1.0.1] - 2019-12-04

### Fixed

- Fix SESSION_REDIS_PORT setting definition

## [eucalyptus.3-wb-1.0.0] - 2019-11-14

### Added

- First experimental release of OpenEdx `eucalyptus.3` (wb flavor).
- Set replicaSet and read_preference in mongodb connection
- Add missing support for redis sentinel

[unreleased]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.10.0...HEAD
[eucalyptus.3-wb-1.10.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.9.4...eucalyptus.3-wb-1.10.0
[eucalyptus.3-wb-1.9.4]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.9.3...eucalyptus.3-wb-1.9.4
[eucalyptus.3-wb-1.9.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.9.2...eucalyptus.3-wb-1.9.3
[eucalyptus.3-wb-1.9.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.9.1...eucalyptus.3-wb-1.9.2
[eucalyptus.3-wb-1.9.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.9.0...eucalyptus.3-wb-1.9.1
[eucalyptus.3-wb-1.9.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.8.1...eucalyptus.3-wb-1.9.0
[eucalyptus.3-wb-1.8.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.8.0...eucalyptus.3-wb-1.8.1
[eucalyptus.3-wb-1.8.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.7.4...eucalyptus.3-wb-1.8.0
[eucalyptus.3-wb-1.7.4]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.7.3...eucalyptus.3-wb-1.7.4
[eucalyptus.3-wb-1.7.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.7.2...eucalyptus.3-wb-1.7.3
[eucalyptus.3-wb-1.7.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.7.1...eucalyptus.3-wb-1.7.2
[eucalyptus.3-wb-1.7.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.7.0...eucalyptus.3-wb-1.7.1
[eucalyptus.3-wb-1.7.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.6.3...eucalyptus.3-wb-1.7.0
[eucalyptus.3-wb-1.6.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.6.2...eucalyptus.3-wb-1.6.3
[eucalyptus.3-wb-1.6.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.6.1...eucalyptus.3-wb-1.6.2
[eucalyptus.3-wb-1.6.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.6.0...eucalyptus.3-wb-1.6.1
[eucalyptus.3-wb-1.6.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.5.0...eucalyptus.3-wb-1.6.0
[eucalyptus.3-wb-1.5.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.4.0...eucalyptus.3-wb-1.5.0
[eucalyptus.3-wb-1.4.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.3.1...eucalyptus.3-wb-1.4.0
[eucalyptus.3-wb-1.3.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.3.0...eucalyptus.3-wb-1.3.1
[eucalyptus.3-wb-1.3.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.2.2...eucalyptus.3-wb-1.3.0
[eucalyptus.3-wb-1.2.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.2.1...eucalyptus.3-wb-1.2.2
[eucalyptus.3-wb-1.2.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.2.0...eucalyptus.3-wb-1.2.1
[eucalyptus.3-wb-1.2.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.1.0...eucalyptus.3-wb-1.2.0
[eucalyptus.3-wb-1.1.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.5...eucalyptus.3-wb-1.1.0
[eucalyptus.3-wb-1.0.5]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.4...eucalyptus.3-wb-1.0.5
[eucalyptus.3-wb-1.0.4]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.3...eucalyptus.3-wb-1.0.4
[eucalyptus.3-wb-1.0.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.2...eucalyptus.3-wb-1.0.3
[eucalyptus.3-wb-1.0.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.1...eucalyptus.3-wb-1.0.2
[eucalyptus.3-wb-1.0.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.0...eucalyptus.3-wb-1.0.1
[eucalyptus.3-wb-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/eucalyptus.3-wb-1.0.0
