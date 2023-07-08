DOMAIN := 'upsala.fandom.se'
IMAGE := 'upsalafandom-builder'

default:
    just --list

build_image:
    podman build -f Containerfile -t '{{ IMAGE }}' .

_in_container *args: build_image
    podman run --rm -it \
    -v "${HOME}/.config/hut:/root/.config/hut:z" \
    -v "{{ justfile_directory() }}:{{ justfile_directory() }}:z" \
    -w "{{ justfile_directory() }}" \
    '{{ IMAGE }}' \
    just IMAGE='{{ IMAGE }}' DOMAIN='{{ DOMAIN }}' {{ args }}

serve:
    podman run --rm -it \
    -v "${HOME}/.config/hut:/root/.config/hut:z" \
    -v "{{ justfile_directory() }}:{{ justfile_directory() }}:z" \
    -w "{{ justfile_directory() }}" \
    -p 1111:1111 \
    '{{ IMAGE }}' \
    zola serve --interface 0.0.0.0

_build:
    #!/bin/bash

    set -xeuo pipefail

    output_dir=''{{ justfile_directory() }}/public''

    rm -rf "${output_dir}"

    zola build --base-url='https://{{ DOMAIN }}'

    find "${output_dir}" -type f -iname '*.html' -not -path "${output_dir}/arkiv/*" \
        -exec tidy \
            --quiet yes \
            --show-warnings no \
            --tidy-mark no \
            --vertical-space no \
            --wrap 0 \
            --write-back yes \
            {} '+' \
            || (($?==1 ? 1 : 0))

    find "${output_dir}" -type f -iname '*.xml' -not -path "${output_dir}/arkiv/*" | while read f; do
        tempfile="$(mktemp -t "$(basename "${f}")".XXXXXXXX)"
        xmlstarlet fo \
            --noindent \
            --nocdata  \
            --nsclean \
            --encode utf-8 \
            "${f}" > "${tempfile}" && mv -v "${tempfile}" "${f}"
    done

build:
    @just IMAGE='{{ IMAGE }}' DOMAIN='{{ DOMAIN }}' _in_container _build

validate: build
    podman run --rm -it \
    -v "{{ justfile_directory() }}:{{ justfile_directory() }}:z" \
    -w "{{ justfile_directory() }}" \
    ghcr.io/validator/validator:latest \
    vnu --skip-non-html public

# FIXME: Add validate as dependency once errors fixed.
package: build
    tar -C public -czf public.tar.gz .

_publish:
    hut pages publish --domain '{{ DOMAIN }}' --site-config ./site-config.json public.tar.gz

publish: package
    @just IMAGE='{{ IMAGE }}' DOMAIN='{{ DOMAIN }}' _in_container _publish

package_redirect:
    tar -C redirect -czf redirect.tar.gz .

_publish_redirect domain: package_redirect
    hut pages publish --domain '{{ domain }}' --site-config ./site-config-redirect.json redirect.tar.gz

publish_redirects:
    @just IMAGE='{{ IMAGE }}' DOMAIN='{{ DOMAIN }}' _in_container _publish_redirect uppsala.fandom.se

check_links:
    podman run --rm docker.io/tennox/linkcheck --external '{{ DOMAIN }}'
