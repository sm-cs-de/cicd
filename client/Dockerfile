FROM python:3.13.7-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY client.py .
COPY tests/test_client.py .

CMD ["python", "client.py"]

