# Copyright 2021 Declarative Systems Pty Ltd
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

# see https://flask.palletsprojects.com/en/1.1.x/patterns/packages/#larger-applications
from artifactory_cloud_proxy import app
from loguru import logger
import requests
from flask import Response
import artifactory_cloud_proxy.config
import artifactory_cloud_proxy.app


@app.app.errorhandler(requests.HTTPError)
def handle_requests_exception(e):
    logger.error(f"http-level requests error: {e}")
    if e.response.status_code == 404:
        message = "not found"
    else:
        message = "error"
    return message, e.response.status_code


@app.app.errorhandler(Exception)
def handle_exception(e):
    logger.exception(e)
    return "upstream error", 500


@app.app.route('/', defaults={'path': ''})
@app.app.route('/<path:path>')
def index(path):
    config = artifactory_cloud_proxy.config.get_config()
    target_url = f"{config[artifactory_cloud_proxy.config.ARTIFACTORY_URL]}{path}"
    logger.info(f"user requested: {path}, downloading artifact: {target_url}")

    r = requests.get(target_url, stream=True)
    r.raise_for_status()

    total_length = r.headers.get('Content-length', -1)
    mime_type = "application/javascript"
    logger.info(f"filesize: {total_length}")

    def generate():
        for chunk in r.iter_content(
                chunk_size=config[artifactory_cloud_proxy.config.CHUNK_SIZE]):
            yield chunk

    return Response(generate(), mimetype=mime_type)
