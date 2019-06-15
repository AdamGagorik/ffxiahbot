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
sphinx-apidoc -o ./generated -f -e -T -M ../../pydarkstar ../../pydarkstar/tests ../../pydarkstar/apps
rm -f ./generated/modules.rst

declare -a stubs=(
    "requirements"
    "setup"
    "usage"
    "advanced"
)

echo ":orphan:" > ./generated/README.rst
echo "" >> ./generated/README.rst
pandoc --from=gfm --to=rst ../../README.md >> ./generated/README.rst

for stub in "${stubs[@]}"; do
    pandoc --from=gfm --to=rst ./markdown/${stub}.md > ./generated/${stub}.rst
    echo ${stub}
done

cd ./generated
python ../scripts/titles.py
python ../scripts/apps.py
cd ..
