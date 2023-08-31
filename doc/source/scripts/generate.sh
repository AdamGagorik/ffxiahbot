#!/bin/bash
set -v
set -e
SDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${SDIR}
cd ..

mkdir -p _static
mkdir -p _templates

rm -rf ./generated
export SPHINX_APIDOC_OPTIONS=members,undoc-members
poetry run sphinx-apidoc -o ./generated -f -e -T -M ../../pydarkstar ../../pydarkstar/tests ../../pydarkstar/apps
rm -f ./generated/modules.rst

cd ./generated
poetry run python ../scripts/titles.py
poetry run python ../scripts/apps.py
cd ..
