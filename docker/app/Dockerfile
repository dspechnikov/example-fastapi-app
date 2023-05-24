FROM python:3.11-slim-bullseye

RUN pip install -q \
        pipenv==2023.5.19 \
        pre-commit==3.3.3 && \
    apt-get update && apt-get install --no-install-recommends -y \
        # git is needed for pre-commit
        git=1:2.30.2-1+deb11u2 \
        # to build postgresql client libraries, i.e. psycopg
        libpq-dev=13.11-0+deb11u1 \
        # wait script to check external services availability, i.e. databases
        wait-for-it=0.0~git20180723-1

ENV \
    # variables set in container shell should override .env file.
    # pipenv prioritizes .env file, so disable its load
    PIPENV_DONT_LOAD_ENV=1 \
    # pipenv cache location to speed up builds
    PIPENV_CACHE_DIR='/var/cache/pipenv'

WORKDIR /app

# install hook environments to cache them for hook runs
COPY .pre-commit-config.yaml /app/
RUN git init && pre-commit install-hooks

COPY Pipfile Pipfile.lock /app/
# mount pipenv cache to speed up builds
RUN --mount=type=cache,target="$PIPENV_CACHE_DIR" \
    pipenv install -d

COPY . /app/
