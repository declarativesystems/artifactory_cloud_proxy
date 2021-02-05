import setuptools
import artifactory_cloud_proxy.version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="artifactory_cloud_proxy",
    version=artifactory_cloud_proxy.version.version,
    author="Geoff Williams",
    author_email="None",
    description="An artifact proxy for Artifactory Cloud (resolves 302 redirects...)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeoffWilliams/artifactory_cloud_proxy.git",
    packages=setuptools.find_packages(),
    # pick from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": []
    },
    include_package_data=True,
    install_requires=[
        'Flask',
        'loguru',
        'requests',
        'validators'
    ]
)
