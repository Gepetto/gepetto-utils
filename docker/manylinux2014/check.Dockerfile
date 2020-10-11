ARG PYVER=3.9
FROM python:$PYVER

ENV PATH=/root/.local/bin:$PATH

RUN apt-get update -qqy \
 && apt-get install -qqy \
    libgl1 \
 && pip install --user \
    jupyter \
    meshcat \
    numpy \
 && pip install --user -i https://test.pypi.org/simple/ \
    eigenpy \
    hpp-fcl \
    pinocchio \
    example-robot-data \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /nb
ADD load_talos.ipynb .
CMD jupyter notebook --allow-root --no-browser --ip='*'
