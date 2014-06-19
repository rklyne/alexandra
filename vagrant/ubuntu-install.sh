#!/bin/bash

apt-get update
apt-get install -y python-setuptools rabbitmq-server python-pygame python-dev
easy_install pip
pip install -U setuptools
pip install -U setuptools pip

pip install pika numpy
service rabbitmq-server start

