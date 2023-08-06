# Development guide


## Install

Currently py27 is the only supported python version. It is recommended that you install this tool within a fresh virtual environment. More info on https://virtualenv.pypa.io/en/stable/userguide/.

```shell
> cd ${repo_root}
> ${envpip} install -r requirements.txt -r requirements_${darwin/linux}.txt
> ${envpip} install .
```

Package depends on `libsodium`. Make sure to install:
```shell
> brew install libsodium # macos
> apt-get install libsodium-dev # linux
```

## Testing

We use [tox](https://tox.readthedocs.io/en/latest/index.html) as the project's test runner. Make sure you have **tox >= 3.5.3** installed in your python environment.

#### Run all tests

```shell
> cd ${repo_core}
> tox
```



#### Unit tests

```shell
> tox -e unit-${darwin/linux}
```



#### Integration tests

```shell
> tox -e integration-${darwin/linux}
```



## Linting

We use [flake8](http://flake8.pycqa.org/en/latest/) as project's linter. Enforcement via:

```shell
> tox -e flake8
```


## Some helper CLIs through make
There are some handy make commands that you can use. Check out usage:

```shell
> cd ${repo-root}
> make
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
	docker-build-runtime: build docker image `relay:${VERSION}` that has installed mail-relay pacakge pulled from pypi
	shell: get interactive shell to builder/tester container

	clean: ...

	publish-pypi: publish package on pypi
	publish-docker-hub: publish image on docker hub
	release: manage release on github, publish on pypi as well as docker hub
]
```

