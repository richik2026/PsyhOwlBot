FROM python:3.12-slim

WORKDIR /app

# Tor is used only as a local fallback SOCKS5 route for Telegram when the
# hosting provider cannot reach api.telegram.org directly.
RUN apt-get update && \
    apt-get install -y --no-install-recommends tor ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Use Timeweb-friendly GitVerse PyPI mirror instead of files.pythonhosted.org.
# This avoids build hangs when direct PyPI downloads time out.
ENV PIP_INDEX_URL=https://pypi-mirror.gitverse.ru/simple/
ENV PIP_DEFAULT_TIMEOUT=300

RUN pip install --upgrade pip && \
    pip install --retries 5 --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
