FROM python:3.11-slim

WORKDIR /tests

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "test_e2e.py", "-v"]
