set -eux

# Don't build wheels for python 3.9
rm -rf /opt/python/cp39-cp39

# Install cmake, ninja and wheel
PY38_BIN=/opt/python/cp38-cp38/bin
$PY38_BIN/pip install cmake ninja wheel
ln -s $PY38_BIN/cmake /usr/bin/
ln -s $PY38_BIN/ninja /usr/bin/
ln -s $PY38_BIN/wheel /usr/bin/

# Upgrade pip and install scikit-build
yum -y install python-pip
pip2 install --upgrade pip
pip2 install scikit-build --user

for PYBIN in /opt/python/*/bin; do
    "$PYBIN"/pip install --upgrade pip
    "$PYBIN"/pip install scikit-build
done
