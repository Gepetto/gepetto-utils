FROM python:3.6-alpine3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /app /static
WORKDIR /app
COPY requirements.txt .

# Get Dependencies
RUN apk update && apk add --virtual deps \
   gcc \
   python-dev \
   linux-headers \
   musl-dev \
   postgresql-dev \
   && apk add --no-cache libpq
RUN pip install -r requirements.txt
RUN apk del deps

COPY . .

# Collect Static
ENV REDMINE_TOKEN=placeholder \
   GITHUB_TOKEN=placeholder \
   DJANGO_SECRET_KEY=placeholder \
   POSTGRES_PASSWORD=placeholder
RUN python manage.py collectstatic
