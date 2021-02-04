test:
	pipenv run pytest

package:
	python setup.py sdist bdist_wheel

upload:
	python -m twine upload dist/*

clean:
	rm dist/*

dev_env:
	pip install -e .

dev_server:
	FLASK_APP=artifactory_cloud_proxy pipenv run flask run

requirements.txt:
	pipenv run pip freeze >> requirements.txt