#!/bin/bash

# USAGE: ./run.sh ( install )

set -o pipefail -o errexit -o nounset -o xtrace

install () {
    pip install beautifulsoup4 markdown pelican pillow
    ./gen_statics_bundles.py || true
}

eval "$1"
