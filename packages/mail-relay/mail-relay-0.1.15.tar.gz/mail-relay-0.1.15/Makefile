define USAGE
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
endef
export USAGE


OS := $(shell uname -s | tr A-Z a-z)
PACKAGE_VERSION := $(shell python setup.py --version)
DEV_VERSION := $(shell git rev-parse HEAD || 'unknown')
RELAY := ./.tox/unit-$(OS)/bin/relay
REPO := samantehrani/relay


VERSION = $(PACKAGE_VERSION)

all:
	@echo "$$USAGE"

clean:
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./.tox


.PHONY: build
build:
	python setup.py sdist


unit-test:
	tox -e unit-$(OS)

integration-test:
	tox -e integration-$(OS)

test: unit-test integration-test

lint:
	tox -e flake8


docker-build:
	docker build -f docker/Dockerfile.builder -t mail-relay-builder .

docker-unit-test: docker-build
	docker run --rm -it mail-relay-builder make unit-test

docker-integration-test: docker-build
	docker run --rm -it mail-relay-builder make integration-test

docker-test: docker-unit-test docker-integration-test

docker-lint: docker-build
	docker run --rm -it mail-relay-builder make lint

docker-build-runtime:
	# fetches $VERSION from pypi, fails if building runting for unpublished version
	# to build specific version -> `make docker-build-runtime VERSION=0.1.3`
	docker build -f docker/Dockerfile --build-arg VERSION=$(VERSION) -t relay:$(VERSION) .


shell:
	docker run --rm -it mail-relay-builder


publish-pypi:
	pip install twine
	make clean
	make test
	make lint
	make gen_usage
	make build VERSION=$(PACKAGE_VERSION)
	twine upload dist/*


publish-docker-hub:
	make clean
	make docker-build-runtime VERSION=$(PACKAGE_VERSION)
	docker tag relay:$(PACKAGE_VERSION) $(REPO):$(PACKAGE_VERSION)
	docker push $(REPO):$(PACKAGE_VERSION)

release:
	@echo 'todo: handle version bump, tag releases on git, merge to master'
	make publish-pypi
	make publish-docker-hub


gen_usage: # depends on built relay pacakge under tox environment.
	echo "## Relay CLI" > docs/usage.md
	$(RELAY) --help >> docs/usage.md

	echo "\r\n#### Config" >> docs/usage.md
	$(RELAY) migrate
	$(RELAY) config --config-file src/mail_relay/config/volume.dev.yml
	$(RELAY) config --help >> docs/usage.md

	echo "\r\n## Make commands" >> docs/usage.md
	echo "$$USAGE" >> docs/usage.md