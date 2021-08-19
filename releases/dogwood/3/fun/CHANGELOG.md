# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

## [dogwood.3-fun-2.3.1] - 2021-08-19

### Fixed

- Update config files in DockerFile even starting from an existing image

## [dogwood.3-fun-2.3.0] - 2021-08-18

### Changed

- Upgrade `fun-apps` to v5.11.0 for protection against VideoFront downtimes

## [dogwood.3-fun-2.2.0] - 2021-07-29

### Fixed

- Fix sources.list for Ubuntu 12.04 moved to old releases

### Removed

- Broken Python development dependencies in Docker development image

### Changed

- Upgrade fun-apps to v5.10.1 to stop synchronizing Elasticsearch index

## [dogwood.3-fun-2.1.1] - 2021-04-13

### Fixed

- Copy newly installed dependencies and modified sources

## [dogwood.3-fun-2.1.0] - 2021-04-12

### Added

- Upgrade fun-apps to v5.9.0

## [dogwood.3-fun-2.0.0] - 2021-04-09

### Changed

- Update Docker build strategy to start from the latest working image

## [dogwood.3-fun-1.18.3] - 2021-02-11

### Fixed

- Upgrade to xblock-proctor-exam to 1.0.0 to fix proctoring after API change
- Fix pip install for python 2.7

### Added

- Upgrade fun-apps to v5.8.0 to automatically add users to a cohort after
  payment and pass course language to course run synchronization hook

## [dogwood.3-fun-1.18.2] - 2021-01-18

### Fixed

- Upgrade fun-apps to v5.7.2 fixing course run synchronization to point to LMS

## [dogwood.3-fun-1.18.1] - 2021-01-18

### Fixed

- Upgrade fun-apps to v5.7.1 to fix course run synchronization for empty dates

## [dogwood.3-fun-1.18.0] - 2021-01-06

### Added

- Upgrade fun-apps to v5.7.0 to allow synchronizing course runs with richie

### Fixed

- Force Django old-release uninstallation due to recent changes in the new
  pip dependencies resolver

## [dogwood.3-fun-1.17.0] - 2020-12-10

### Added

- Add new `PLATFORM_RICHIE_URL` setting in lms config used by fun-apps

### Changed

- Enable CORS requests

## [dogwood.3-fun-1.16.0] - 2020-12-04

### Changed

- Upgrade fun-apps to v5.6.0 to enable connection with richie

## [dogwood.3-fun-1.15.2] - 2020-11-10

### Fixed

- Fix missing `DEFAULT_COURSE_ABOUT_IMAGE_URL` setting in cms config

## [dogwood.3-fun-1.15.1] - 2020-10-22

### Fixed

- Upgrade fun-apps to v5.5.1 to fix `update_courses` command when some course
  have an invalid key

## [dogwood.3-fun-1.15.0] - 2020-10-02

### Added

- Upgrade to fun-apps v5.5.0 to allow placing thumbnail related media files
  behind the CDN

## [dogwood.3-fun-1.14.2] - 2020-10-01

### Fixed

- Upgrade to fun-apps v5.4.2 to fix thumbnails related 500 when filesystem down

## [dogwood.3-fun-1.14.1] - 2020-09-08

### Fixed

- Pin django-classy-tags to 0.8.0 to avoid breaking changes

## [dogwood.3-fun-1.14.0] - 2020-09-07

### Added

- Add Gelf support for logging

## [dogwood.3-fun-1.13.2] - 2020-09-01

### Fixed

- Pin splinter to 0.13.0 to avoid breaking change in 0.14.0
- Adjust settings to support `REDIS_SERVICE=redis-sentinel`

## [dogwood.3-fun-1.13.1] - 2020-07-20

### Changed

- Upgrade `fun-apps` to `5.4.1`

## [dogwood.3-fun-1.13.0] - 2020-05-14

### Added

- Allow serving static files via a CDN

### Changed

- Collect static files in the `edxapp` image so it can run without mounting a volume
  for its static files in Kubernetes

## [dogwood.3-fun-1.12.1] - 2020-04-08

### Changed

- Set basic authentification backend for development environment

### Fixed

- Pin `django-redis` to version 4.5.0

## [dogwood.3-fun-1.12.0] - 2020-04-07

### Added

- Add `django-redis-sentinel-redux` to allow the use of Redis Sentinel for
  Django cache

### Changed

- Configure most Django cache backends to Redis

### Removed

- Remove now useless Memcached settings

## [dogwood.3-fun-1.11.0] - 2020-04-01

### Changed

- Upgrade `fun-apps` to `5.4.0` to add a "browsable" status for courses in the catalog

## [dogwood.3-fun-1.10.0] - 2020-03-25

### Added

- Rate limiting authentication backend that works behind proxies

### Changed

- Refactor the way authentication backends are configured to make it straightforward

## [dogwood.3-fun-1.9.2] - 2020-03-13

### Fixed

- Fix setting AUTHENTICATION_BACKENDS to allow activating third party authentication
- Downgrade and pin `virtualenv` to version 16.7.9

## [dogwood.3-fun-1.9.1] - 2020-01-29

### Fixed

- Upgrade `fun-apps` to `5.3.1` to further accelerate the home page for authenticated users
- Remove hardcoded FILE_UPLOAD_STORAGE_BUCKET_NAME value to make sure it is configurable

## [dogwood.3-fun-1.9.0] - 2020-01-29

### Changed

- Upgrade `fun-apps` to `5.3.0` to cache home page for authenticated users

## [dogwood.3-fun-1.8.6] - 2020-01-23

### Fixed

- Upgrade `fun-apps` to `5.2.2`

## [dogwood.3-fun-1.8.5] - 2020-01-22

### Fixed

- Certificates are in a directory with a french name: "attestations"

## [dogwood.3-fun-1.8.4] - 2020-01-21

### Fixed

- Rewrite settings related to FUN's certificates download URLs
- Fixed known unpacking bug by upgrading to openfun/edx-platform version dogwood.3-fun-5.3.1

## [dogwood.3-fun-1.8.3] - 2020-01-17

### Fixed

- Set MEDIA_ROOT in cms config as it is used to generate thumbnails in `fun-apps`

## [dogwood.3-fun-1.8.2] - 2020-01-17

### Fixed

- Upgrade FUN's `edx-platform` release to `v5.3.0` (deactivate logging
  anonymous user id error)

## [dogwood.3-fun-1.8.1] - 2020-01-11

### Removed

- Checks that ensure required directories exist in volumes

## [dogwood.3-fun-1.8.0] - 2020-01-10

### Added

- Make Gunicorn workers and threads configurable via an environment variable

### Fixed

- Ensure all required directories exist inside each volume

## [dogwood.3-fun-1.7.0] - 2020-01-08

### Changed

- Upgrade fun-apps to 5.2.0

### Fixed

- Add missing `fun` application templates directory to default templates directories
  to activate `videoupload` templates
- Configure all cache backends as they are in FUN's production instance

## [dogwood.3-fun-1.6.0] - 2020-01-03

### Changed

- Stop inheriting from MKTG_URL_LINK_MAP default setting
- Relocate FUN certificates to media files instead of specific volume
- Refactor FUN settings as fine tuning that comes after the main settings

### Fixed

- Add missing installed app `masquerade` for support staff to impersonate users

## [dogwood.3-fun-1.5.1] - 2019-12-27

### Fixed

- Refactor settings to repair and clean what is cms versus lms, edx versus
  fun-apps, configurable versus defined by code.

## [dogwood.3-fun-1.5.0] - 2019-12-26

### Added

- Make Gunicorn timeout configurable via an environment variable

### Fixed

- Move LTI xblock configurations from fun settings to production

## [dogwood.3-fun-1.4.2] - 2019-12-26

### Fixed

- Allow configuring the configurable LTI consumer xblock

### Security

- Remove selftest from installed apps to stop exposing settings on a url

## [dogwood.3-fun-1.4.1] - 2019-12-24

### Fixed

- `AUTH_TOKENS` was wrongly used as a dictionary and default values were lost

## [dogwood.3-fun-1.4.0] - 2019-12-19

### Added

- Force edX to use `libcast_xblock` as default video xblock
- Use custom demo course for FUN's flavors

### Fixed

- Add missing setting `LMS_ROOT_URL` used to compute absolute urls
- Fix `GITHUB_REPO_ROOT` and `DATA_DIR` settings

## [dogwood.3-fun-1.3.8] - 2019-12-16

### Fixed

- Fix broken CMS JS build by enabling Pipeline's static files storage

## [dogwood.3-fun-1.3.7] - 2019-12-16

### Fixed

- Configure `general` cache backend including cache keys sanitizing function

## [dogwood.3-fun-1.3.6] - 2019-12-15

### Fixed

- Properly configure locales
- Use pyOpenSSL instead of local openssl library for SSL certificate checking

## [dogwood.3-fun-1.3.5] - 2019-12-12

### Changed

- Declare redis as the default session engine

### Added

- Add Glowbl xblock settings

## [dogwood.3-fun-1.3.4] - 2019-12-10

### Fixed

- Fix redis release compatibility with celery-redis-sentinel (_e.g._ redis
  2.x.x)
- Remove unusable static and media-related paths from settings.yml

## [dogwood.3-fun-1.3.3] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [dogwood.3-fun-1.3.2] - 2019-12-05

### Changed

- Switch ORA2 production backend to Swift
- Make `CELERY_RESULT_BACKEND` configurable

## [dogwood.3-fun-1.3.1] - 2019-12-04

### Fixed

- Fix SESSION_REDIS_PORT setting definition

## [dogwood.3-fun-1.3.0] - 2019-12-02

### Added

- Add missing support for redis sentinel

## [dogwood.3-fun-1.2.1] - 2019-11-29

### Fixed

- Add missing RELEASE setting

## [dogwood.3-fun-1.2.0] - 2019-11-22

### Added

- Set replicaSet and read_preference in mongodb connection

## [dogwood.3-fun-1.1.0] - 2019-11-22

### Added

- FUN production settings carefully splitted between python and yaml files

## [dogwood.3-fun-1.0.0] - 2019-11-07

### Added

- First experimental release of OpenEdx `dogwood.3` (fun flavor).

[unreleased]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-2.3.1...HEAD
[dogwood.3-fun-2.3.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-2.3.0...dogwood.3-fun-2.3.1
[dogwood.3-fun-2.3.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-2.2.0...dogwood.3-fun-2.3.0
[dogwood.3-fun-2.2.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-2.1.1...dogwood.3-fun-2.2.0
[dogwood.3-fun-2.1.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-2.1.0...dogwood.3-fun-2.1.1
[dogwood.3-fun-2.1.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-2.0.0...dogwood.3-fun-2.1.0
[dogwood.3-fun-2.0.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.18.3...dogwood.3-fun-2.0.0
[dogwood.3-fun-1.18.3]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.18.2...dogwood.3-fun-1.18.3
[dogwood.3-fun-1.18.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.18.1...dogwood.3-fun-1.18.2
[dogwood.3-fun-1.18.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.18.0...dogwood.3-fun-1.18.1
[dogwood.3-fun-1.18.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.17.0...dogwood.3-fun-1.18.0
[dogwood.3-fun-1.17.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.16.0...dogwood.3-fun-1.17.0
[dogwood.3-fun-1.16.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.15.2...dogwood.3-fun-1.16.0
[dogwood.3-fun-1.15.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.15.1...dogwood.3-fun-1.15.2
[dogwood.3-fun-1.15.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.15.0...dogwood.3-fun-1.15.1
[dogwood.3-fun-1.15.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.14.2...dogwood.3-fun-1.15.0
[dogwood.3-fun-1.14.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.14.1...dogwood.3-fun-1.14.2
[dogwood.3-fun-1.14.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.14.0...dogwood.3-fun-1.14.1
[dogwood.3-fun-1.14.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.13.2...dogwood.3-fun-1.14.0
[dogwood.3-fun-1.13.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.13.1...dogwood.3-fun-1.13.2
[dogwood.3-fun-1.13.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.13.0...dogwood.3-fun-1.13.1
[dogwood.3-fun-1.13.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.12.1...dogwood.3-fun-1.13.0
[dogwood.3-fun-1.12.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.12.0...dogwood.3-fun-1.12.1
[dogwood.3-fun-1.12.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.11.0...dogwood.3-fun-1.12.0
[dogwood.3-fun-1.11.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.10.0...dogwood.3-fun-1.11.0
[dogwood.3-fun-1.10.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.9.2...dogwood.3-fun-1.10.0
[dogwood.3-fun-1.9.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.9.1...dogwood.3-fun-1.9.2
[dogwood.3-fun-1.9.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.9.0...dogwood.3-fun-1.9.1
[dogwood.3-fun-1.9.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.6...dogwood.3-fun-1.9.0
[dogwood.3-fun-1.8.6]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.5...dogwood.3-fun-1.8.6
[dogwood.3-fun-1.8.5]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.4...dogwood.3-fun-1.8.5
[dogwood.3-fun-1.8.4]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.3...dogwood.3-fun-1.8.4
[dogwood.3-fun-1.8.3]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.2...dogwood.3-fun-1.8.3
[dogwood.3-fun-1.8.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.1...dogwood.3-fun-1.8.2
[dogwood.3-fun-1.8.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.8.0...dogwood.3-fun-1.8.1
[dogwood.3-fun-1.8.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.7.0...dogwood.3-fun-1.8.0
[dogwood.3-fun-1.7.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.6.0...dogwood.3-fun-1.7.0
[dogwood.3-fun-1.6.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.5.1...dogwood.3-fun-1.6.0
[dogwood.3-fun-1.5.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.5.0...dogwood.3-fun-1.5.1
[dogwood.3-fun-1.5.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.4.2...dogwood.3-fun-1.5.0
[dogwood.3-fun-1.4.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.4.1...dogwood.3-fun-1.4.2
[dogwood.3-fun-1.4.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.4.0...dogwood.3-fun-1.4.1
[dogwood.3-fun-1.4.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.8...dogwood.3-fun-1.4.0
[dogwood.3-fun-1.3.8]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.7...dogwood.3-fun-1.3.8
[dogwood.3-fun-1.3.7]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.6...dogwood.3-fun-1.3.7
[dogwood.3-fun-1.3.6]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.5...dogwood.3-fun-1.3.6
[dogwood.3-fun-1.3.5]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.4...dogwood.3-fun-1.3.5
[dogwood.3-fun-1.3.4]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.3...dogwood.3-fun-1.3.4
[dogwood.3-fun-1.3.3]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.2...dogwood.3-fun-1.3.3
[dogwood.3-fun-1.3.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.1...dogwood.3-fun-1.3.2
[dogwood.3-fun-1.3.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.0...dogwood.3-fun-1.3.1
[dogwood.3-fun-1.3.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.2.1...dogwood.3-fun-1.3.0
[dogwood.3-fun-1.2.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.2.0...dogwood.3-fun-1.2.1
[dogwood.3-fun-1.2.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.1.0...dogwood.3-fun-1.2.0
[dogwood.3-fun-1.1.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.0.0...dogwood.3-fun-1.1.0
[dogwood.3-fun-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/dogwood.3-fun-1.0.0
