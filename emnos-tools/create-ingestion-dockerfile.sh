#!/usr/bin/env bash

cat << EOF >> ./emnos-tools/ingestion.dockerfile

FROM $LATEST_BASE_IMAGE:$LATEST_BASE_IMAGE_TAG

USER emnos
ENV HOME=/home/emnos
ENV PATH="$HOME/.local/bin:$PATH"
WORKDIR /opt/emnosapp/private-gpt

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY --chown=emnos:emnos . /opt/emnosapp/private-gpt

RUN poetry install --extras "llms-gemini embeddings-gemini ui vector-stores-qdrant" --no-interaction --no-ansi \
    && pip install  --no-cache-dir -e .

ENTRYPOINT ["bash", "-c", "make wipe && make ingest $INGEST_FOLDER"]


EOF

exit 0
