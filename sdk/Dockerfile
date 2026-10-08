# Soul Cradle document-evaluation SDK
# Build from the repo root: docker build -t soul-cradle-sdk -f sdk/Dockerfile .
# Run:   docker run --rm -v "$PWD/docs:/docs" soul-cradle-sdk /docs/report.pdf --out /docs/evaluation.json
FROM python:3.11-slim

WORKDIR /app
COPY soul_cradle/ ./soul_cradle/
COPY sdk/ ./sdk/
RUN pip install --no-cache-dir pypdf

ENV PYTHONPATH=/app:/app/sdk
ENTRYPOINT ["python", "-m", "soul_cradle_sdk.cli"]
