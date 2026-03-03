# === Builder: llama-cpp-python (long compilation, cached separately) ===
FROM python:3.12-slim AS builder-llm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

ARG LLAMA_CPP_VERSION=0.3.16
RUN pip install --no-cache-dir --prefix=/install llama-cpp-python==${LLAMA_CPP_VERSION}

# === Builder: other Python deps ===
FROM python:3.12-slim AS builder-deps

COPY --from=builder-llm /install /usr/local

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# === Piper download ===
FROM debian:trixie-slim AS piper-dl

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ARG PIPER_VERSION=2023.11.14-2
RUN curl -L -o /tmp/piper.tar.gz \
    "https://github.com/rhasspy/piper/releases/download/${PIPER_VERSION}/piper_linux_x86_64.tar.gz" \
    && mkdir -p /opt/piper \
    && tar -xzf /tmp/piper.tar.gz -C /opt \
    && rm /tmp/piper.tar.gz

# === Runtime ===
FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libespeak-ng1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder-llm /install /usr/local
COPY --from=builder-deps /install /usr/local
COPY --from=piper-dl /opt/piper /opt/piper
ENV PATH="/opt/piper:${PATH}"

WORKDIR /app

COPY app/ ./app/

RUN mkdir -p /tmp/audiocoach

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# === Test ===
FROM runtime AS test

RUN pip install --no-cache-dir pytest pytest-asyncio httpx

COPY tests/ ./tests/
COPY pyproject.toml .

CMD ["python", "-m", "pytest", "tests/", "-v"]
