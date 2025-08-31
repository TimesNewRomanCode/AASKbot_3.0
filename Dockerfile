FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libreoffice \
    default-jre \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["python", "-u", "main.py"]