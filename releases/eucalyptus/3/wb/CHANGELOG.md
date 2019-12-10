# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Fixed

- Fix redis release compatibility with celery-redis-sentinel (_e.g._ redis
  2.x.x)

## [eucalyptus.3-1.0.2-wb] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [eucalyptus.3-1.0.1-wb] - 2019-12-04

### Fixed

- Fix SESSION_REDIS_PORT setting definition

## [eucalyptus.3-1.0.0-wb] - 2019-11-14

### Added

- First experimental release of OpenEdx `eucalyptus.3` (wb flavor).
- Set replicaSet and read_preference in mongodb connection
- Add missing support for redis sentinel

[unreleased]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.2-wb...HEAD
[eucalyptus.3-1.0.2-wb]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.1-wb...eucalyptus.3-1.0.2-wb
[eucalyptus.3-1.0.1-wb]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.0-wb...eucalyptus.3-1.0.1-wb
[eucalyptus.3-1.0.0-wb]: https://github.com/openfun/openedx-docker/releases/tag/eucalyptus.3-1.0.0-wb
