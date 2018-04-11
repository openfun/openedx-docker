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

## Running FUN's unit tests

    docker-compose exec lms-dev python manage.py lms test --settings=fun.docker_run_lms_test

    docker-compose exec cms-dev python manage.py cms test --settings=fun.docker_run_cms_test

# Docker images

The plan is to prepare several lines of images, the docker files and settings of which are living in its own branch (e.g. ginkgo.1, eucalyptus-funwb, dogwood-funmooc,...)

Branch names on the current repository are of the form: **{edx-version}[-{fork-name}]**
Two words separated by a dash, the second word being optional:
- **edx-version:** name of the upstream `edx-platform` version (e.g. ginkgo.1),
- **fork-name:** name of the specific project fork, if any (e.g. funwb).

We are pushing to `DockerHub` only images that are the result of a tag respecting the pattern: **{branch-name}-x.y.z**

Here are some valid examples:

- dogwood.3-1.0.3
- dogwood.2-funmooc-17.6.1
- eucalyptus-funwb-2.3.19


## TODO list

- Investigate why the CMD does not received system signals,
- Add missing services (ecommerce, forum, xqueue),
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
