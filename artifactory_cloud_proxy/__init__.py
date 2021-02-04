# see https://flask.palletsprojects.com/en/1.1.x/patterns/packages/#larger-applications
from flask import Flask
app = Flask(__name__)

import artifactory_cloud_proxy.views