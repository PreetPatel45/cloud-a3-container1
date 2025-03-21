FROM python:3.9-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY app1.py .

CMD ["python", "app1.py"]