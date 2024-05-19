#!/bin/bash

set -xeuo pipefail

rm -rf "${OUTPUT_DIR}"

zola build --base-url="https://${DOMAIN}"

find "${OUTPUT_DIR}" -type f -iname '*.html' -not -path "${OUTPUT_DIR}/arkiv/*" \
    -exec tidy \
        --quiet yes \
        --show-warnings no \
        --tidy-mark no \
        --vertical-space no \
        --wrap 0 \
        --write-back yes \
        {} '+' \
        || (($?==1 ? 1 : 0))

find "${OUTPUT_DIR}" -type f -iname '*.xml' -not -path "${OUTPUT_DIR}/arkiv/*" | while read f; do
    tempfile="$(mktemp -t "$(basename "${f}")".XXXXXXXX)"
    xmlstarlet fo \
        --noindent \
        --nocdata  \
        --nsclean \
        --encode utf-8 \
        "${f}" > "${tempfile}" && mv -v "${tempfile}" "${f}"
done
