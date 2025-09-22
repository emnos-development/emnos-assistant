#!/usr/bin/env bash

cat << EOF >> ./emnos-tools/dockerfile

FROM $LATEST_BASE_IMAGE:$LATEST_BASE_IMAGE_TAG

RUN mkdir -p /opt/emnosapp/private-gpt \
    && chown -R emnos:emnos /opt/emnosapp/private-gpt

USER emnos
ENV HOME=/home/emnos
ENV PATH="/home/emnos/.local/bin:$PATH"
WORKDIR /opt/emnosapp/private-gpt

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY --chown=emnos:emnos . /opt/emnosapp/private-gpt

COPY --chown=emnos:emnos ./local_data/private_gpt/qdrant /opt/emnosapp/private-gpt/local_data/qdrant

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry install --extras "llms-gemini embeddings-gemini ui vector-stores-qdrant" --no-interaction --no-ansi \
    && pip install -e .

EXPOSE 8080
ENTRYPOINT ["bash", "-c", "PGPT_PROFILES=gemini make run"]

EOF

exit 0
