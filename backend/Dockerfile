FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Use Timeweb-friendly GitVerse PyPI mirror instead of files.pythonhosted.org.
# This avoids build hangs when direct PyPI downloads time out.
ENV PIP_INDEX_URL=https://pypi-mirror.gitverse.ru/simple/
ENV PIP_DEFAULT_TIMEOUT=300

RUN pip install --upgrade pip && \
    pip install --retries 5 --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
