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

## [hawthorn.1-oee-3.3.4] - 2021-03-04

### Fixed

- Fix ORA2 urls that were breaking assets
- Fix pip install for python 2.7

## [hawthorn.1-oee-3.3.3] - 2020-11-20

### Fixed

- Hide broken file links on ORA2 upload widget

## [hawthorn.1-oee-3.3.2] - 2020-11-09

### Fixed

- Make ORA2 work with the filesystem backend

## [hawthorn.1-oee-3.3.1] - 2020-09-01

### Fixed

- Pin `django-redis` version to `4.5.0` to be able to use
  `django-redis-sentinel-redux`.
- Adjust settings to support `REDIS_SERVICE=redis-sentinel`

## [hawthorn.1-oee-3.3.0] - 2020-05-14

### Added

- Allow serving static files via a CDN
- Add `django-redis-sentinel-redux` to allow the use of Redis Sentinel for
  Django cache

### Changed

- Collect static files in the `edxapp` image so it can run without mounting a volume
  for its static files in Kubernetes
- Configure most Django cache backends to Redis

### Removed

- Remove now useless Memcached settings

## [hawthorn.1-oee-3.2.0] - 2020-04-08

### Added

- Rate limiting authentication backend that works behind proxies

### Changed

- Refactor the way authentication backends are configured to make it straightforward
- Set basic authentification backend for development environment

### Fixed

- Remove hardcoded FILE_UPLOAD_STORAGE_BUCKET_NAME value to make sure it is configurable

## [hawthorn.1-oee-3.1.2] - 2020-01-23

### Fixed

- Copy `webpack-stats.json` files to expected static files root path in case no
  static files volume is mounted

## [hawthorn.1-oee-3.1.1] - 2020-01-22

### Fixed

- Generate `edxapp-nginx` companion

## [hawthorn.1-oee-3.1.0] - 2020-01-15

### Changed

- Upgrade to a recent release of nodejs as the one packaged in Ubuntu was breaking the build

### Removed

- Checks that ensure required directories exist in volumes

## [hawthorn.1-oee-3.0.0] - 2020-01-10

### Added

- Configure all cache backends
- Make Gunicorn timeout, workers and threads configurable via an environment
  variable

### Changed

- Move DATA_DIR to same location as for other flavors (breaking change)
- Make ORA2 configurable and use filesystem backend by default
- Stop inheriting from MKTG_URL_LINK_MAP default setting

### Fixed

- Ensure all required directories exist inside each volume
- Make Celery result backend configurable

## [hawthorn.1-oee-2.12.3] - 2019-12-10

### Fixed

- Fix redis release compatibility with celery-redis-sentinel (_e.g._ redis
  2.x.x)

## [hawthorn.1-oee-2.12.2] - 2019-12-05

### Fixed

- Use the plugin celery-redis-sentinel to introduce the support of
  redis sentinel in celery instead of upgrading celery itself.

## [hawthorn.1-oee-2.12.1] - 2019-12-04

### Fixed

- Fix SESSION_REDIS_PORT setting definition

## [hawthorn.1-oee-2.12.0] - 2019-12-02

### Added

- Add missing support for redis sentinel

## [hawthorn.1-oee-2.11.0] - 2019-11-22

### Added

- Set replicaSet and read_preference in mongodb connection

## [hawthorn.1-oee-2.10.1] - 2019-10-25

### Fixed

- Restore LOCALE_PATHS override for the LMS

## [hawthorn.1-oee-2.10.0] - 2019-10-10

### Changed

- Add LOCALE_PATHS to configurable settings
- Remove useless timezone configuration
- Remove useless development dependencies
- Upgraded
  [fonzie](https://github.com/openfun/fonzie)
  to
  [`v0.2.1`](https://github.com/openfun/fonzie/releases/tag/v0.2.1)

### Fixed

- Restore LMS's instructor exported files support and fonzie's integration in
  development

## [hawthorn.1-oee-2.9.1] - 2019-06-04

### Fix

- Add missing Django Rest Framework setting required by Fonzie's API.

## [hawthorn.1-oee-2.9.0] - 2019-05-23

### Added

- Add [Fonzie](https://github.com/openfun/fonzie)
  [`v0.2.0`](https://github.com/openfun/fonzie/releases/tag/v0.2.0)
  to activate an ACL endpoint to control access to LMS instructor
  dashboard exported files

## [hawthorn.1-oee-2.8.2] - 2019-03-19

### Changed

- Upgraded
  [xblock-configurable-lti-consumer](https://github.com/openfun/xblock-configurable-lti-consumer)
  to
  [`v1.2.3`](https://github.com/openfun/xblock-configurable-lti-consumer/releases/tag/v1.2.3)

## [hawthorn.1-oee-2.8.1] - 2019-03-06

### Added

- Allow configuring credentials separately (oauth_consumer_key and
  shared_secret), so we don't need to encrypt all settings to hide secrets

### Changed

- Upgraded
  [xblock-configurable-lti-consumer](https://github.com/openfun/xblock-configurable-lti-consumer)
  to
  [`v1.2.2`](https://github.com/openfun/xblock-configurable-lti-consumer/releases/tag/v1.2.2)

### Fixed

- Fix getting fields values when defaults or hidden fields are not defined

## [hawthorn.1-oee-2.8.0] - 2019-02-25

### Added

- Install `lynx` to perform HTML to text conversions

## [hawthorn.1-oee-2.7.0] - 2019-02-14

### Added

- Give precedence to a passport defined in the course over the passport defined
  in our settings
- Allow presetting the iframe height with a correct ratio to avoid a black box
  flickering when the iFrame containing the LTI service loads

### Changed

- Upgraded
  [xblock-configurable-lti-consumer](https://github.com/openfun/xblock-configurable-lti-consumer)
  to
  [`v1.2.1`](https://github.com/openfun/xblock-configurable-lti-consumer/releases/tag/v1.2.1)

### Fixed

- Allow setting visible fields dynamically from the Studio (hidden fields are
  still taken from the configuration in settings)

## [hawthorn.1-oee-2.6.0] - 2019-02-08

### Added

- Make memcached host & port configurable

## [hawthorn.1-oee-2.5.1] - 2019-01-31

### Fixed

- Use default common setting for `TRACKING_IGNORE_URL_PATTERNS`

## [hawthorn.1-oee-2.5.0] - 2019-01-21

### Changed

- Upgrade XBlock configurable LTI consumer to 1.1.0 (it allows to generate LTI
  launch urls dynamically on the basis of a regex)

## [hawthorn.1-oee-2.4.1] - 2019-01-18

### Fixed

- Upgrade XBlock configurable LTI consumer to `1.0.0-rc.3`

## [hawthorn.1-oee-2.3.0] - 2018-12-20

### Changed

- Install `gettext` system dependency so that Django can work on translations

### Fixed

- Configure system locale to `en_US.UTF-8` to prevent Python encoding issues

## [hawthorn.1-oee-2.2.1] - 2018-12-18

### Fixed

- Fix cache invalidation bugs between the CMS and the LMS by configuring
  `memcache` as a cache backend (shared between pods).

## [hawthorn.1-oee-2.2.0] - 2018-12-11

### Changed

- Use Redis for sessions

### Fixed

- Fix `STATIC_ROOT_BASE`

## [hawthorn.1-oee-2.1.1] - 2018-11-29

### Fixed

- Fix logging environment in Sentry

## [hawthorn.1-oee-2.1.0] - 2018-11-28

### Changed

- Upgrade edx-platform (oee flavor) to `hawthorn.1-1.0.0-rc.1` (includes our
  configurable LTI XBlock)

## [hawthorn.1-oee-2.0.3] - 2018-11-20

### Changed

- Improve Sentry configuration (add `environment` and `release` information to
  our Sentry events)

## [hawthorn.1-oee-2.0.2] - 2018-11-15

### Changed

- Upgrade `edx-platform` dependency to `oee/hawthorn.1-0.1.3`

## [hawthorn.1-oee-2.0.1] - 2018-11-12

First release of OpenEdx extended.

### Added

- Add a configurable LTI consumer xblock

[unreleased]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.3.4..HEAD
[hawthorn.1-oee-3.3.4]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.3.3...hawthorn.1-oee-3.3.4
[hawthorn.1-oee-3.3.3]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.3.2...hawthorn.1-oee-3.3.3
[hawthorn.1-oee-3.3.2]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.3.1...hawthorn.1-oee-3.3.2
[hawthorn.1-oee-3.3.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.3.0...hawthorn.1-oee-3.3.1
[hawthorn.1-oee-3.3.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.2.0...hawthorn.1-oee-3.3.0
[hawthorn.1-oee-3.2.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.1.2...hawthorn.1-oee-3.2.0
[hawthorn.1-oee-3.1.2]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.1.1...hawthorn.1-oee-3.1.2
[hawthorn.1-oee-3.1.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.1.0...hawthorn.1-oee-3.1.1
[hawthorn.1-oee-3.1.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-3.0.0...hawthorn.1-oee-3.1.0
[hawthorn.1-oee-3.0.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.12.3...hawthorn.1-oee-3.0.0
[hawthorn.1-oee-2.12.3]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.12.2...hawthorn.1-oee-2.12.3
[hawthorn.1-oee-2.12.2]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.12.1...hawthorn.1-oee-2.12.2
[hawthorn.1-oee-2.12.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.12.0...hawthorn.1-oee-2.12.1
[hawthorn.1-oee-2.12.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.11.0...hawthorn.1-oee-2.12.0
[hawthorn.1-oee-2.11.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.10.1...hawthorn.1-oee-2.11.0
[hawthorn.1-oee-2.10.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.10.0...hawthorn.1-oee-2.10.1
[hawthorn.1-oee-2.10.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.9.1...hawthorn.1-oee-2.10.0
[hawthorn.1-oee-2.9.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.9.0...hawthorn.1-oee-2.9.1
[hawthorn.1-oee-2.9.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.8.2...hawthorn.1-oee-2.9.0
[hawthorn.1-oee-2.8.2]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.8.1...hawthorn.1-oee-2.8.2
[hawthorn.1-oee-2.8.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.8.0...hawthorn.1-oee-2.8.1
[hawthorn.1-oee-2.8.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.7.0...hawthorn.1-oee-2.8.0
[hawthorn.1-oee-2.7.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.6.0...hawthorn.1-oee-2.7.0
[hawthorn.1-oee-2.6.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.5.1...hawthorn.1-oee-2.6.0
[hawthorn.1-oee-2.5.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.5.0...hawthorn.1-oee-2.5.1
[hawthorn.1-oee-2.5.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.4.1...hawthorn.1-oee-2.5.0
[hawthorn.1-oee-2.4.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.3.0...hawthorn.1-oee-2.4.1
[hawthorn.1-oee-2.3.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.2.1...hawthorn.1-oee-2.3.0
[hawthorn.1-oee-2.2.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.2.0...hawthorn.1-oee-2.2.1
[hawthorn.1-oee-2.2.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.1.1...hawthorn.1-oee-2.2.0
[hawthorn.1-oee-2.1.1]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.1.0...hawthorn.1-oee-2.1.1
[hawthorn.1-oee-2.1.0]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.0.3...hawthorn.1-oee-2.1.0
[hawthorn.1-oee-2.0.3]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.0.2...hawthorn.1-oee-2.0.3
[hawthorn.1-oee-2.0.2]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-oee-2.0.1...hawthorn.1-oee-2.0.2
[hawthorn.1-oee-2.0.1]: https://github.com/openfun/openedx-docker/releases/tag/hawthorn.1-oee-2.0.1
