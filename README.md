# Flask Api Starter Kit [![CircleCI](https://circleci.com/gh/aranginw/flask-api-starter-kit/tree/master.svg?style=svg)](https://circleci.com/gh/aranginw/flask-api-starter-kit/tree/master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aranginw/flask-api-starter-kit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aranginw/flask-api-starter-kit/?branch=master)

This starter kit is designed to allow you to create very fast your Flask API. It was forked from https://github.com/aranginw/flask-api-starter-kit and the plan is to add components more specific to the way I develop. Their work is an awesome starting point.

The primary goal of this project is to remain as **unopinionated** as possible. Its purpose is not to dictate your project structure or to demonstrate a complete sample application, but to provide a set of tools intended to make back-end development robust, easy, and, most importantly, fun.

This starter kit comes with a [tutorial](https://github.com/aranginw/flask-api-starter-kit/blob/tutorial/doc/installation.md).
Check it out if you want a quick tutorial on how to use Flask with this architecure.

## Table of Contents

- [Flask Api Starter Kit ![CircleCI](https://circleci.com/gh/aranginw/flask-api-starter-kit/tree/master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/aranginw/flask-api-starter-kit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/aranginw/flask-api-starter-kit/?branch=master)](#flask-api-starter-kit-img-srchttpscirclecicomgharanginwflask-api-starter-kittreemastersvgstylesvg-altcircleci-img-srchttpsscrutinizer-cicomgaranginwflask-api-starter-kitbadgesquality-scorepngbmaster-altscrutinizer-code-quality)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
  - [Getting Started](#getting-started)
  - [Commands](#commands)
  - [Database](#database)
    - [Initialize](#initialize)
  - [Application Structure](#application-structure)
  - [Development](#development)
  - [Testing](#testing)
  - [Lint](#lint)
  - [Format](#format)
  - [Swagger](#swagger)

## Dependencies

You will need [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

## Getting Started

First, clone the project:

```bash
$ git clone https://github.com/aranginw/flask-api-starter-kit.git <my-project-name>
$ cd <my-project-name>
```

Then install dependencies and check that it works

```bash
$ make server.install      # Install the pip dependencies on the docker container
$ make server.start        # Run the container containing your local python server
```


If everything works, you should see the available routes [here](http://127.0.0.1:3000/application/spec).

The API runs locally on docker containers. You can easily change the python version you are willing to use [here](https://github.com/aranginw/flask-api-starter-kit/blob/master/docker-compose.yml#L4), by fetching a docker image of the python version you want.

Locally, you can create a python virtual environment and install all dependencies for local development purposes.
```bash
$ python -m venv .venv     # This creates a virtual env in current dir
$ pip install -r requirements-dev.txt
```
`.gitignore` is already set up to ignore `.venv`, so if you're goint to change the name of this directory, be sure to change it in `.gitignore` as well.

## Commands

You can display availables make commands using `make`.

While developing, you will probably rely mostly on `make server.start`; however, there are additional scripts at your disposal:

| `make <script>`      | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| `help`               | Display availables make commands                                             |
| `server.install`     | Install the pip dependencies on the server's container.                      |
| `server.start`       | Run your local server in its own docker container.                           |
| `server.daemon`      | Run your local server in its own docker container as a daemon.               |
| `server.upgrade`     | Upgrade pip packages interactively.                                          |
| `database.connect`   | Connect to your docker database.                                             |
| `database.migrate`   | Generate a database migration file using alembic, based on your model files. |
| `database.upgrade`   | Run the migrations until your database is up to date.                        |
| `database.downgrade` | Downgrade your database by one migration.                                    |
| `test`               | Run unit tests with pytest in its own container.                             |
| `test.coverage`      | Run test coverage using pytest-cov.                                          |
| `test.lint`          | Run flake8 on the `src` and `test` directories.                              |
| `test.safety`        | Run safety to check if your vendors have security issues.                    |
| `format.black`       | Format python files using Black.                                             |
| `format.isort`       | Order python imports using isort.                                            |

## Database

The database is in [PostgreSql](https://www.postgresql.org/).

Locally, you can connect to your database using :

```bash
$ make database.connect
```

### Initialize
Your first `make server.start` command will set up the entire system including the application database. The credentials can be set in the `.env` file located at the root of the project directory.

You will need to run `make database.upgrade` to run all the migrations and get the database up to date.

Connect to the database using `make database.connect`. This will put you in a psql shell in the DB container.

Hint: If you are having problems, try to run `make server.nuke` to start from scratch and then `make server.start` again. The database initialization script only runs on a fresh new setup, so sometimes if you have artifacts around, it may prevent the init script from running (found in `src/scripts/init.sh`). 


We are database versioning using [alembic](https://pypi.python.org/pypi/alembic).
Once you've changed your models, which should reflect your database's state, you can generate the migration, then upgrade or downgrade your database as you want. See [Commands](#commands) for more information.

The migration will be generated by the container, it may possible that you can only edit it via `sudo` or by running `chown` on the generated file.

## Application Structure

The application structure presented in this boilerplate is grouped primarily by file type. Please note, however, that this structure is only meant to serve as a guide, it is by no means prescriptive.

```
.
├── devops                   # Project devops configuration settings
│   └── deploy               # Environment-specific configuration files for shipit
├── migrations               # Database's migrations settings
│   └── versions             # Database's migrations versions generated by alembic
├── src                      # Application source code
│   ├── models               # Python classes modeling the database
│   │   ├── abc.py           # Abstract base class model
│   │   └── user.py          # Definition of the user model
│   ├── repositories         # Python classes allowing you to interact with your models
│   │   └── user.py          # Methods to easily handle user models
│   ├── resources            # Python classes containing the HTTP verbs of your routes
│   │   └── user.py          # Rest verbs related to the user routes
│   ├── routes               # Routes definitions and links to their associated resources
│   │   ├── __init__.py      # Contains every blueprint of your API
│   │   └── user.py          # The blueprint related to the user
│   ├── swagger              # Resources documentation
│   │   └── user             # Documentation of the user resource
│   │       └── GET.yml      # Documentation of the GET method on the user resource
│   ├── util                 # Some helpfull, non-business Python functions for your project
│   │   └── parse_params.py  # Wrapper for the resources to easily handle parameters
│   ├── config.py            # Project configuration settings
│   ├── manage.py            # Project commands
│   └── server.py            # Server configuration
└── test                     # Unit tests source code
```

## Development

To develop locally, here are your two options:

```bash
$ make server.start           # Create the containers containing your python server in your terminal
$ make server.daemon          # Create the containers containing your python server as a daemon
```

The containers will reload by themselves as your source code is changed.
You can check the logs in the `./server.log` file.

## Testing

To add a unit test, simply create a `test_*.py` file anywhere in `./test/`, prefix your test classes with `Test` and your testing methods with `test_`. Unittest will run them automaticaly.
You can add objects in your database that will only be used in your tests, see example.
You can run your tests in their own container with the command:

```bash
$ make test
```

## Lint

To lint your code using flake8, just run in your terminal:

```bash
$ make test.lint
```

It will run the flake8 commands on your project in your server container, and display any lint error you may have in your code.

## Format

The code is formatted using [Black](https://github.com/python/black) and [Isort](https://pypi.org/project/isort/). You have the following commands to your disposal:

```bash
$ make format.black # Apply Black on every file
$ make format.isort # Apply Isort on every file
```

## Swagger

Your API needs a description of it's routes and how to interact with them.
You can easily do that with the swagger package included in the starter kit.
Simply add a docstring to the resources of your API like in the `user` example.
The API description will be available [here](http://127.0.0.1:3000/application/spec).
The Swagger UI will be available [here](http://127.0.0.1:3000/apidocs/).
