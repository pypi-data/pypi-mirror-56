## Relay CLI
Usage: relay [OPTIONS] COMMAND [ARGS]...

  relay is a simple cli tool that relays preveil emails to a configurable
  smtp server

Options:
  -p, --store-path FILE    Path to sqlite store.  [default:
                           /Users/sk/developement/mail-relay/relay.sqlite]
  --store-version INTEGER  sqlite store version.  [default: 0]
  --help                   Show this message and exit.

Commands:
  config   Show existing configiguration or re-config an existing setup.
  info     Show information about organization, export groups and members.
  migrate  Migrate database using mail_rely/migrate.py (or optional script).
  start    Start relay daemon.
  status   Check status of relay daemon

#### Config
Usage: relay config [OPTIONS] COMMAND [ARGS]...

  Show existing configiguration or re-config an existing setup.

Options:
  -c, --config-file FILE
  --help                  Show this message and exit.

Commands:
  approver  Configure organization export group approver accounts
  exporter  Configure organization export group expoter account
  user      Configure organization exporter account

## Make commands
USAGE:
> make [
	build: build python package
	unit-test: run unit tests with tox
	integration-test: run integration tests with tox
	test: run all tests
	lint: run flake8 linter with tox

	docker-build: build python package in a linux container
	docker-unit-test: run unit tests with tox in a linux container
	docker-integration-test: run integration tests with tox in a linux container
	docker-test: run all tests in a linux container
	docker-build-runtime: build docker image `relay:0.1.16` that has installed mail-relay pacakge pulled from pypi
	shell: get interactive shell to builder/tester container

	clean: ...

	publish-pypi: publish package on pypi
	publish-docker-hub: publish image on docker hub
	release: manage release on github, publish on pypi as well as docker hub
]
