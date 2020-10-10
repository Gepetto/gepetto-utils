ARG PYVER=3.7
FROM python:$PYVER

RUN apt-get update -qqy && apt-get install -qqy libgl1 && rm -rf /var/lib/apt/lists/* && pip install --user --no-cache-dir numpy

ADD dist config test.sh /
CMD /test.sh
