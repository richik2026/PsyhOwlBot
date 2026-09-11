FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

ENV PIP_INDEX_URL=https://pypi-mirror.gitverse.ru/simple/
ENV PIP_DEFAULT_TIMEOUT=300

RUN pip install --upgrade pip && \
    pip install --retries 5 --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start_bot.sh

CMD ["sh", "start_bot.sh"]
