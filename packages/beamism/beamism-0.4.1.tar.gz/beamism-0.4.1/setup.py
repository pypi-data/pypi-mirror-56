# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages


REQUIRED_PACKAGES = [
    'apache-beam>=2.16.0',
    'jsonschema>=3.2.0',
    'dill>=0.3.0',
    'dnspython>=1.15.0',
    # 'grpc-google-iam-v1<0.13dev,>=0.12.3',
    # 'gapic-google-cloud-pubsub-v1>=0.15.4',
    'gitpython>=3.0.5',
    'google-api-core>=1.1.2',
    'google-apitools<0.5.29,>=0.5.28',
    'google-auth>=1.4.1',
    'google-auth-httplib2>=0.0.3',
    'google-cloud-core>=0.25.0',
    'google-cloud-pubsub>=0.26.0',
    # 'google-gax>=0.15.16',
    'googleapis-common-protos>=1.5.3',
    'oauth2client>=3.0.0',
    #    'proto-google-cloud-pubsub-v1>=0.15.4',
    'python-dateutil>=2.7.3',
    'pymongo>=3.6.1',
    'slackclient>=2.3.1'
]


with open('version.cache', 'r') as f:
    version = f.read()


setup(
    name="beamism",
    version=version,
    packages=find_packages(),
    description='welcome to beamism',
    platforms='Linux, Darwin',
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ]
)
