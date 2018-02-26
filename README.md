# WIP

# FUN PLATFORM

`FUN PLATFORM` introduces an alternative `Docker` approach to install a complete and customized version of **[Open edX](https://open.edx.org)**. The idea is to use `Docker` without `Ansible`, in order to make the project simpler, more flexible and fully operable by developpers.

**We hope this kind of `Docker` configuration can soon be included in the edx-platform repository itself.**


## Approach

This project builds docker images that are ready for production. `Docker compose` is only used for development purposes so that we can code locally and see our changes immediately:

- Sources and configuration files are mounted from the host,
- The Docker CMD launches runserver instead of gunicorn,
- Ports are opened on the application containers to allow bypassing nginx.

Docker compose also allows us to run a complete project in development, including database services which in production are not run on Docker. See the [docker-compose file](./docker-compose.yml) for details on each service:

- **mysql:** the SQL database used to structure and persist the application data,
- **mongodb:** the no-SQL database used to store course content,
- **memcached:** the cache engine,
- **rabbitmq:** the messaging broker used for asynchronous tasks,
- **lms:** the Django web application used by learners,
- **cms:** the Django web application used by teachers,
- **forum:** the Ruby web application serving the discussion forum, **TODO**
- **ecommerce:** the Django web application used for payments, **TODO**
- **xqueue:** the interface for the LMS to communicate with external grader services, **TODO**
- **nginx:** the front end web server configured to serve static/media files and proxy other requests to Django.


## Getting started

Make sure you have a recent version of [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install) installed on your laptop:

    $ docker -v
      Docker version 17.12.0-ce, build c97c6d6

    $ docker-compose --version
      docker-compose version 1.17.1, build 6d101fb

⚠️ `Docker Compose` version 1.19 is not supported because of a bug (see https://github.com/docker/compose/issues/5686). Please downgrade to 1.18 or upgrade to a higher version.

Start the full project by running:

    $ make bootstrap

You should now be able to view the web applications:

- LMS:
    * served by runserver: [localhost:8072](http://localhost:8072)
    * served by nginx: [localhost:8073](http://localhost:8073)
- CMS:
    * served by runserver: [localhost:8082](http://localhost:8082)
    * served by nginx: [localhost:8083](http://localhost:8083)

See other available commands by running:

    $ make


## TODO list

- Investigate why the CMD does not received system signals,
- Add missing services (ecommerce, forum, xqueue),
- Run `paver update_assets --skip-collect` from within the Dockerfile and run `collectstatic` only after deployment to production,
- Make use of Docker multi-stage builds to remove build tools from the production Docker image (node_modules, nodejs, git, python-pip, etc.),
- Improve Python dependencies on [edx-platform](https://github.com/edx/edx-platform).

### About this last point

Docker's best practices could not be applied completely because of the way edx-platform manages dependencies. Build time on code updates with this PR is a few minutes depending on your connection, not too bad. But we could make it nearly immediate with some refactoring to the way edx-platform handles dependencies.

If you want to understand further, build the project with `make all`. When it's done, cd into `src/edx-platform` and modify the `.gitignore` file to keep only the `*.pyc` rule. Now run `git status` to see all the files that have been modified as a result of running `pip install requirements/local.txt` (last step of the Docker file).

These modifications to the repository:

- force us to reinstall the last step when mounting the source files from host (which is required for development in order to see our changes immediately). Not hard but hackish and unexpected,
- forces Docker to reinstall the last step on each build. We could speed up build time to make it almost instantaneous.
- is a bit obscure for the new comer because it is not a common pattern. Dependencies and project code are usually kept separate. 

Maybe improving this is not so hard and the benefits could be big.

For reference, here is the output of the `git status` command after removing gitignore:

```
    .prereqs_cache/
    Open_edX.egg-info/
    cms/envs/production.py
    common/lib/calc/calc.egg-info/
    common/lib/capa/capa.egg-info/
    common/lib/chem/chem.egg-info/
    common/lib/dogstats/dogstats_wrapper.egg-info/
    common/lib/safe_lxml/safe_lxml.egg-info/
    common/lib/sandbox-packages/sandbox_packages.egg-info/
    common/lib/symmath/symmath.egg-info/
    common/lib/xmodule/XModule.egg-info/
    common/static/bundles/
    common/static/common/js/vendor/
    lms/envs/production.py
    lms/static/certificates/css/
    lms/static/css/bootstrap/
    lms/static/css/discussion/
    lms/static/css/lms-course-rtl.css
    lms/static/css/lms-course.css
    lms/static/css/lms-footer-edx-rtl.css
    lms/static/css/lms-footer-edx.css
    lms/static/css/lms-footer-rtl.css
    lms/static/css/lms-footer.css
    lms/static/css/lms-learner-dashboard-rtl.css
    lms/static/css/lms-learner-dashboard.css
    lms/static/css/lms-main-v1-rtl.css
    lms/static/css/lms-main-v1.css
    lms/static/css/lms-main-v2-rtl.css
    lms/static/css/lms-main-v2.css
    node_modules/
    openedx/core/lib/xblock_builtin/xblock_discussion/xblock_discussion.egg-info/
    themes/red-theme/lms/static/css/bootstrap/
    themes/red-theme/lms/static/css/discussion/
    themes/red-theme/lms/static/css/lms-course-rtl.css
    themes/red-theme/lms/static/css/lms-course.css
    themes/red-theme/lms/static/css/lms-footer-edx-rtl.css
    themes/red-theme/lms/static/css/lms-footer-edx.css
    themes/red-theme/lms/static/css/lms-footer-rtl.css
    themes/red-theme/lms/static/css/lms-footer.css
    themes/red-theme/lms/static/css/lms-learner-dashboard-rtl.css
    themes/red-theme/lms/static/css/lms-learner-dashboard.css
    themes/red-theme/lms/static/css/lms-main-v1-rtl.css
    themes/red-theme/lms/static/css/lms-main-v1.css
    themes/red-theme/lms/static/css/lms-main-v2-rtl.css
    themes/red-theme/lms/static/css/lms-main-v2.css
    themes/stanford-style/lms/static/css/bootstrap/
    themes/stanford-style/lms/static/css/discussion/
    themes/stanford-style/lms/static/css/lms-course-rtl.css
    themes/stanford-style/lms/static/css/lms-course.css
    themes/stanford-style/lms/static/css/lms-footer-edx-rtl.css
    themes/stanford-style/lms/static/css/lms-footer-edx.css
    themes/stanford-style/lms/static/css/lms-footer-rtl.css
    themes/stanford-style/lms/static/css/lms-footer.css
    themes/stanford-style/lms/static/css/lms-learner-dashboard-rtl.css
    themes/stanford-style/lms/static/css/lms-learner-dashboard.css
    themes/stanford-style/lms/static/css/lms-main-v1-rtl.css
    themes/stanford-style/lms/static/css/lms-main-v1.css
    themes/stanford-style/lms/static/css/lms-main-v2-rtl.css
    themes/stanford-style/lms/static/css/lms-main-v2.css
```