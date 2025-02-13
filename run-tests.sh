#!/bin/bash

PYTHON="${PYTHON:-python3.12}"

set -e

export PIP_EXTRA_INDEX_URL=https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple
export UV_EXTRA_INDEX_URL=https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple

OAREPO_VERSION="${OAREPO_VERSION:-12}"

BUILDER_VENV=.venv-builder
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

$PYTHON -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -U oarepo-model-builder oarepo-model-builder-files

if test -d records2 ; then
  rm -rf records2
fi

oarepo-compile-model ./tests/records2.yaml --output-directory records2 --profile record,files -vvv

VENV=".venv"

if test -d $VENV ; then
  rm -rf $VENV
fi

$PYTHON -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel

pip install "oarepo[tests, rdm]==${OAREPO_VERSION}.*"
pip install -e ".[tests]"
pip install -e records2

if [ a"$1"==a"--docker" ] ; then
docker rm -f test-services-cache-1 test-services-s3-1 test-services-search-1 test-services-db-1
docker compose -f docker-compose-tests.yml up -d

while true ; do
  curl 127.0.0.1:9200/cat/_indices && break || true
  sleep 1
done

fi

pytest -s -vv tests/