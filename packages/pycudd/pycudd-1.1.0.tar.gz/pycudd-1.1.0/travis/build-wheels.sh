#!/bin/bash
echo "Running build-wheels.sh"

set -e -x

# Install a system package required by our library
yum install -y swig

# Compile wheels
#find /opt/python | grep pip$

# Omit python 2.6
SUPPORTED_PYTHONS=$(ls /opt/python | grep -v cp26)

for PYBIN in $SUPPORTED_PYTHONS; do
    PIP=/opt/python/${PYBIN}/bin/pip

    echo Running: $PIP install -r /io/dev-requirements.txt
    $PIP install -r /io/dev-requirements.txt
    
    echo Running: $PIP wheel /io/ -w wheelhouse/
    $PIP wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
echo Running: ls wheelhouse/
ls wheelhouse/
for whl in wheelhouse/*.whl; do
    auditwheel repair $whl -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in $SUPPORTED_PYTHONS; do
    PIP=/opt/python/${PYBIN}/bin/pip
    $PIP install python-manylinux-demo --no-index -f /io/wheelhouse
    (cd $HOME; ${PYBIN}/bin/nosetests pymanylinuxdemo)
done

ls io/wheelhouse
