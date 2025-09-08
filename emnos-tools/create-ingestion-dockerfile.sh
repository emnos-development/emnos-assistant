#!/usr/bin/env bash

cat << EOF >> ./emnos-tools/ingestion.dockerfile

FROM $LATEST_BASE_IMAGE:$LATEST_BASE_IMAGE_TAG

RUN mkdir -p /opt/emnosapp/private-gpt \
    && chown -R emnos:emnos /opt/emnosapp/private-gpt

USER emnos
ENV HOME=/home/emnos
ENV PATH="/home/emnos/.local/bin:$PATH"
WORKDIR /opt/emnosapp/private-gpt

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY --chown=emnos:emnos . /opt/emnosapp/private-gpt

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry install --extras "llms-gemini embeddings-gemini ui vector-stores-qdrant" --no-interaction --no-ansi \
    && pip install -e .

ENTRYPOINT ["bash", "-c", "make wipe && make ingest ${INGEST_FOLDER}"]


EOF

exit 0
