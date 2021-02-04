# see https://flask.palletsprojects.com/en/1.1.x/patterns/packages/#larger-applications
from artifactory_cloud_proxy import app
from loguru import logger
import requests
from flask import Response

ARTIFACTORY_URL=os.environ['ARTIFACTORY_URL']
#"https://declarativesystems.jfrog.io/artifactory/"
CHUNK_SIZE=1024


@app.errorhandler(requests.HTTPError)
def handle_requests_exception(e):
    logger.error(f"http-level requests error: {e}")
    if e.response.status_code == 404:
        message = "not found"
    else:
        message = "error"
    return message, e.response.status_code


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"caught exception: {e}")
    return "upstream error", 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    target_url = f"{ARTIFACTORY_URL}{path}"
    logger.info(f"user requested: {path}, downloading artifact: {target_url}")

    r = requests.get(target_url, stream=True)
    r.raise_for_status()
    # try:
    total_length = r.headers.get('Content-length', -1)
    mime_type = "application/javascript"
    logger.info(f"filesize: {total_length}")

    def generate():
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            yield chunk

    return Response(generate(), mimetype=mime_type)
    # except requests.exceptions.HTTPError as e:
    #     raise RuntimeException("not found")
    # except requests.exceptions.RequestException as e:
    #     raise RuntimeException("upstream error")