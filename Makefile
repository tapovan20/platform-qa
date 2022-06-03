#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2019-2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

# This is the Makefile for the platform-qa repo. Based on from genctl/Acadia-service-workspace

curr_dir := $(shell pwd)
USER := $(shell echo $$USER)

BUILD_TIME := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
GIT_SHA    := $(shell git rev-parse --verify HEAD || echo "unknown")
SHORT_GIT_SHA    := $(shell git rev-parse --short --verify HEAD || echo "unknown")
export GIT_SHA SHORT_GIT_SHA
GIT_SHA_DATE := $(shell git show -s --format=%ci HEAD || echo "unknown")
export GIT_SHA_DATE
GIT_BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD || echo "unknown")
export GIT_BRANCH_NAME
BUILD_REPO=local

ifdef $$TRAVIS_PULL_REQUEST
	TRAVIS_PULL_REQUEST := $$TRAVIS_PULL_REQUEST
endif

ifdef $$TRAVIS
	TRAVIS := $$TRAVIS
endif

ifdef $$TRAVIS_COMMIT
	TRAVIS_COMMIT := $$TRAVIS_COMMIT
endif

ifdef $$TRAVIS_PULL_REQUEST_SLUG
	TRAVIS_PULL_REQUEST_SLUG := $$TRAVIS_PULL_REQUEST_SLUG
	BUILD_REPO = $(shell echo $${TRAVIS_PULL_REQUEST_SLUG} | tr '[:upper:]' '[:lower:]')
endif

ifdef $$TRAVIS_BRANCH
	TRAVIS_BRANCH = $$TRAVIS_BRANCH
endif

ifndef $$TRAVIS_PULL_REQUEST_BRANCH
	local_branch = $(shell git branch --no-color |grep '*' | cut -d ' ' -f 2)
	WORKING_BRANCH = $(shell echo $${TRAVIS_BRANCH:=${local_branch}} | tr '[:upper:]' '[:lower:]')
else
	WORKING_BRANCH = ${TRAVIS_COMMIT}
endif

ACADIA_USER ?= $(shell echo $$USER | tr '[:upper:]' '[:lower:]')
ACADIA_REPO ?= wcp-acadia-team-docker-virtual.artifactory.swg-devops.com

BASE_VERSION=$(shell cat VERSION)

OS_IMAGE=$(shell cat OS_CONTAINER | grep OS_IMAGE | cut -f 2 -d '=')
OS_VERSION=$(shell cat OS_CONTAINER | grep OS_VERSION | cut -f 2 -d '=')

OS_BUILD_IMAGE=${ACADIA_REPO}/${OS_IMAGE}
OS_BUILD_VERSION=${OS_VERSION}

ifeq ($(TRAVIS_BRANCH),master)
  ifdef $$TRAVIS_COMMIT_RANGE
	TRAVIS_COMMIT_RANGE = $$TRAVIS_COMMIT_RANGE
  endif

  ifeq ($(TRAVIS_COMMIT_RANGE),${EMPTY})
    COMMIT_OPTION = -2
  else
	COMMIT_OPTION = $(shell echo ${TRAVIS_COMMIT_RANGE} | cut -f 1,4 -d '.' --output-delimiter '..')
  endif
else
  COMMIT_OPTION = "origin/master..${WORKING_BRANCH}"
endif

# On PR we can not pull from an authenticated REPO,
# This is to deal with that.
ifneq ($(TRAVIS_PULL_REQUEST),false)
  OS_SAFE_VERSION=$(shell echo ${OS_VERSION} | awk '{split($$0,a,"-"); print a[1]"-"a[2]}')
  OS_BUILD_IMAGE=${OS_IMAGE}
  OS_BUILD_VERSION=${OS_SAFE_VERSION}
endif



DOCKER_NO_CACHE ?=
ifdef CI
  DOCKER_NO_CACHE = "--no-cache"
endif

ifeq ($(TRAVIS),true)
  TRAVIS_BUILD_NUMBER = $(shell echo $${TRAVIS_BUILD_NUMBER})
  CONT_NAME = $(shell echo "$${TRAVIS_PULL_REQUEST_SLUG:=$${TRAVIS_REPO_SLUG}}" | tr '[:upper:]' '[:lower:]')
  CONT_VERS = ${BASE_VERSION}.build-${TRAVIS_BUILD_NUMBER}
else
  CONT_NAME = ${ACADIA_USER}/platform-qa
  CONT_VERS = ${BASE_VERSION}.dev.${SHORT_GIT_SHA}
endif

## all: Build evertyhing
.PHONY: all
all: base-container test

## clean: clean up local images and artifacts
.PHONY: clean
clean:
	find . -name __pycache__ -type d -delete
	(images=$$(docker image ls |grep platform-qa|awk '{print $$3}') \
		&& echo $$images \
		&& docker image rm -f $$images || true)


bin/qa-containers.tgz: Dockerfile.rf-ceph $(wildcard robot/*)
	docker build \
		${DOCKER_NO_CACHE} \
		-f Dockerfile.rf-ceph \
		-t genctl-acadia/platform-qa-robot:latest .
	docker build \
		${DOCKER_NO_CACHE} \
		-f Dockerfile.perf-ceph \
		-t genctl-acadia/platform-qa-performance:latest .
	./tools/save_images.sh

## image: Build the acadia-platform-qa image
.PHONY: image
image: bin/qa-containers.tgz
	docker build \
		--build-arg SHORT_SHA=${SHORT_GIT_SHA} \
		--build-arg OS_IMAGE=${OS_BUILD_IMAGE} \
		--build-arg OS_VERSION=${OS_BUILD_VERSION} \
		--build-arg BUILD_VERSION=${CONT_VERS} \
		--build-arg BUILD_SHA=${GIT_SHA} \
		--build-arg BUILD_REPO=${BUILD_REPO} \
		${DOCKER_NO_CACHE} \
		-t ${CONT_NAME}:${CONT_VERS} .

.PHONY: test-container
test-container: image requirements-test.txt
	docker build -f Dockerfile.test \
		${DOCKER_NO_CACHE} \
		--build-arg BASE_OS=${CONT_NAME} \
		--build-arg BASE_OS_VER=${CONT_VERS} \
		-t ${CONT_NAME}:test .

## test: Test and Lint code
.PHONY: test
test: pytest
	$(info At some point we should testing and linting etc.)

## lint: Validate code is in proper format
.PHONY: lint
lint: pycodestyle commit_enforce
	$(info helper to just run all linters)

## commit_enforce: Validate that the commit messages conform to standards
.PHONY: commit_enforce
commit_enforce:
	git log ${COMMIT_OPTION} --oneline | python tools/check_commit.py

.PHONY: pycodestyle
pycodestyle: test-container
	docker run -v $${PWD}:/src -w /src \
		${CONT_NAME}:test pycodestyle -v

## pytest: Run python unit tests
.PHONY: pytest
pytest: test-container
	docker run -v $${PWD}:/src -w /src \
		${CONT_NAME}:test pytest

## dev_push_image: Publish container into the docker registry for devs
.PHONY: dev_push_image
dev_push_image: image
	docker tag ${CONT_NAME}:${CONT_VERS} ${ACADIA_REPO}/${CONT_NAME}:${CONT_VERS}
	docker push ${ACADIA_REPO}/${CONT_NAME}:${CONT_VERS}

## push_image: Publish container into the docker registry
.PHONY: push_image
push_image: image
	# tag build
	docker tag ${CONT_NAME}:${CONT_VERS} ${ACADIA_REPO}/${CONT_NAME}:${CONT_VERS}
	docker push ${ACADIA_REPO}/${CONT_NAME}:${CONT_VERS}

.PHONY: help
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
