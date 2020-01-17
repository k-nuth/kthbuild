#!/bin/bash
#
# Copyright (c) 2020 Fernando Pelliccioni
#
set -e
set -x

python --version

if [[ $TRAVIS_PYTHON_VERSION == 2.7 ]]; then
    export KTH_PYTHON=python
    export KTH_PIP=pip
else
    sudo apt-get update
    sudo apt-get --yes install python3.7
    sudo apt-get --yes install python3.7-dev

    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3.7 get-pip.py
    export KTH_PYTHON=python3.7
    export KTH_PIP=pip3.7
fi

sudo $KTH_PIP install --upgrade pip
sudo $KTH_PIP install --upgrade wheel
sudo $KTH_PIP install --upgrade twine
sudo $KTH_PIP install --upgrade setuptools 


# if [[ "${TRAVIS_BRANCH}" == "dev" ]]; then
#     # Just for dev branch
#     sudo $KTH_PIP install --upgrade --index-url https://test.pypi.org/pypi/ cpuid-native
# fi    

cd /home/conan/project

# sudo $KTH_PIP install -v -e .
sudo $KTH_PIP install -e .

# if [[ "${UNIT_TESTS}" == "true" ]]; then
#     $KTH_PYTHON test/test_chain.py
# fi    

if [[ "${UPLOAD_PKG}" == "true" ]]; then
    sudo $KTH_PYTHON setup.py sdist
    sudo $KTH_PYTHON setup.py bdist_wheel --universal
fi    
