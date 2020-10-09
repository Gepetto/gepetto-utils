ARG PYVER=3.7
FROM python:$PYVER

RUN apt-get update -qqy && apt-get install -qqy libgl1 && rm -rf /var/lib/apt/lists/*

ADD dist config test.sh /
CMD /test.sh
