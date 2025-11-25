FROM python:3.13.7-slim
WORKDIR /app

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/server.py .
COPY tests/test_server.py .

CMD ["python", "server.py"]

