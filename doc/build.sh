#!/usr/bin/env bash
set -v
set -e
SDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${SDIR}

./source/scripts/generate.sh
poetry run poetry-dynamic-versioning
poetry run sphinx-build -b html -d build/doctrees source build/html
