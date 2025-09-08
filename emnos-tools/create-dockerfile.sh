#!/usr/bin/env bash

cat << EOF >> ./emnos-tools/dockerfile

FROM $LATEST_BASE_IMAGE:$LATEST_BASE_IMAGE_TAG

USER emnos
ENV HOME=/home/emnos
ENV PATH="$HOME/.local/bin:$PATH"
WORKDIR /opt/emnosapp/private-gpt

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY --chown=emnos:emnos . /opt/emnosapp/private-gpt

COPY --chown=emnos:emnos ./local_data/private_gpt/qdrant /opt/emnosapp/private-gpt/local_data/qdrant

RUN poetry install --extras "llms-gemini embeddings-gemini ui vector-stores-qdrant" --no-interaction --no-ansi \
    && pip install  --no-cache-dir -e .

EXPOSE 8080
ENTRYPOINT ["bash", "-c", "PGPT_PROFILES=gemini make run"]

EOF

exit 0
