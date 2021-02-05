# Copyright 2020 Declarative Systems Pty Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# =========================================================================
# You must set ARTIFACTORY_URL environment variable when running this image
# =========================================================================

FROM docker.io/python:3.9.1-buster

ARG ARTIFACTORY_CLOUD_PROXY_VERSION


COPY dist/artifactory_cloud_proxy-${ARTIFACTORY_CLOUD_PROXY_VERSION}-py3-none-any.whl \
    /app/artifactory_cloud_proxy-${ARTIFACTORY_CLOUD_PROXY_VERSION}-py3-none-any.whl
COPY uwsgi.ini /app
RUN pip install /app/artifactory_cloud_proxy-${ARTIFACTORY_CLOUD_PROXY_VERSION}-py3-none-any.whl
RUN pip install uwsgi

ENTRYPOINT ["uwsgi", "/app/uwsgi.ini"]
