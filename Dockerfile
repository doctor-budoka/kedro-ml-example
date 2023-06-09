FROM python:3.10.10

# Configure Poetry
ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

ENV APP_HOME=/usr/kedro_ml/
CMD mkdir ${APP_HOME}

WORKDIR ${APP_HOME}
COPY poetry.lock ${APP_HOME}
COPY pyproject.toml ${APP_HOME}
RUN poetry install
COPY ./ ${APP_HOME}
