#!/usr/bin/env bash
conda activate pydarkstar
./source/scripts/generate.sh
sphinx-build -b html -d build/doctrees source build/html
