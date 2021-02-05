git_rev := $(shell git rev-parse --short HEAD)
# remove leading 'v'
# the currently checked out tag or 0.0.0=
git_tag := $(shell git describe --tags 2> /dev/null | cut -c 2- | grep -E '.+')

ci_image_name := quay.io/declarativesystems/artifactory_cloud_proxy
ARTIFACTORY_CLOUD_PROXY_VERSION := $(shell python artifactory_cloud_proxy/version.py)
ifdef git_tag
	# on a release tag
	final_version = $(git_tag)
else
	# snapshot build
	final_version = $(ARTIFACTORY_CLOUD_PROXY_VERSION)-$(git_rev)
endif

test:
	pipenv run pytest

package:
	python setup.py sdist bdist_wheel

upload:
	python -m twine upload dist/*

upload_artifactory:
	pip install -r requirements.txt
	python setup.py bdist_wheel upload -r local

clean:
	rm dist/*

dev_env:
	pip install -e .

dev_server:
	FLASK_APP=artifactory_cloud_proxy.app pipenv run flask run

requirements.txt:
	pipenv run pip freeze >> requirements.txt

print_version:
	@python artifactory_cloud_proxy/version.py

image_build:
	buildah bud \
		--format docker \
		-t $(ci_image_name):$(final_version) \
		--build-arg ARTIFACTORY_CLOUD_PROXY_VERSION=$(ARTIFACTORY_CLOUD_PROXY_VERSION) \
		.

image_run:
ifndef ARTIFACTORY_URL
	@echo "ARTIFACTORY_URL environment variable missing"
	exit 1
endif
	podman run \
		--name artifactory_cloud_proxy \
		--rm \
		-e ARTIFACTORY_URL=$(ARTIFACTORY_URL) \
		-v $(shell pwd):/mnt \
		-p9090:9090 \
		-ti $(ci_image_name):$(final_version)


shell:
	podman run \
		-p9090:9090 \
		--rm \
		-v $(shell pwd):/mnt \
		--entrypoint /bin/bash \
		-ti $(ci_image_name):$(final_version)

# shell inside the CI container
ci_shell:
	@echo "project files will be available at /mnt"
	podman run --rm -v $(shell pwd):/mnt -ti \
		--privileged \
		$(shell yq e '.pipelines.[0].configuration.runtime.image.custom.name' pipelines.yml):$(shell yq e '.pipelines.[0].configuration.runtime.image.custom.tag' pipelines.yml) \
		/bin/bash


ci_image_push:
	podman push $(ci_image_name):$(final_version)

.PHONY: requirements.txt