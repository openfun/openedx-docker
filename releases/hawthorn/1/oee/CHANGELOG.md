# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Changed

- Remove useless timezone configuration
- Remove useless development dependencies

## [hawthorn.1-oee-2.9.1] - 2019-06-04

### Fix

- Add missing Django Rest Framework setting required by Fonzie's API.

## [hawthorn.1-oee-2.9.0] - 2019-05-23

### Added

- Add [Fonzie](https://github.com/openfun/fonzie) `0.2.0` to activate an ACL
  endpoint to control access to LMS instructor dashboard exported files

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

[unreleased]: https://github.com/openfun/openedx-docker/compare/hawthorn.1-2.6.0...HEAD
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
