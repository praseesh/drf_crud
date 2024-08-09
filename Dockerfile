FROM python:3.10-slim

COPY requirement.txt /app/
COPY src /app/

WORKDIR /app/

RUN pip install -r requirement.txt

CMD uvicorn main:app --host 0.0.0.0 --port 8000