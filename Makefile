IMAGE := localhost/upsalafandom-builder:latest

export DOMAIN := upsala.fandom.se
export OUTPUT_DIR := public

PODMAN := podman run --rm -it \
	--volume "$(HOME)/.config/hut:/root/.config/hut:z" \
	--volume "$(CURDIR):$(CURDIR):Z" \
	--workdir "$(CURDIR)"

.PHONY: all image build serve validate package publish package_redirect publish_redirect check_links

all:
	make --print-targets

image:
	podman build -f Containerfile -t $(IMAGE) .

build: image
	$(PODMAN) --env DOMAIN --env OUTPUT_DIR $(IMAGE) bash build.sh

serve: image
	$(PODMAN) --publish '1111:1111' $(IMAGE) zola serve --interface 0.0.0.0

validate: build
	$(PODMAN) ghcr.io/validator/validator:latest vnu --skip-non-html public

package: build
	tar -C public -czf public.tar.gz .

publish: package
	$(PODMAN) $(IMAGE) hut pages publish --domain $(DOMAIN) --site-config ./site-config.json public.tar.gz

package_redirect:
	tar -C redirect -czf redirect.tar.gz .

publish_redirect: package_redirect
	$(PODMAN) $(IMAGE) hut pages publish --domain uppsala.fandom.se --site-config ./site-config-redirect.json redirect.tar.gz

check_links:
	$(PODMAN) docker.io/tennox/linkcheck:latest --external $(DOMAIN)
