import setuptools

setuptools.setup(
    name="needle-forms",
    version="0.0.8",
    author="dmiranda",
    author_email="dmiranda@ciandt.com",
    description="Abstraction layer to GCP resources",
    url="https://github.com/ciandt-dev/needle-forms",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'google-cloud-datastore>=1.8.0',
        'google-cloud-pubsub>=0.41.0',
        'google-cloud-bigquery>=1.21.0',
        'pydal==20190915.2',
        'PyMySQL==0.9.3',
        'pg8000==1.13.2',
    ],
)
