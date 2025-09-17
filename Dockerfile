FROM python:3.11-slim

WORKDIR /app
COPY app.py .

RUN pip install flask requests

EXPOSE 8080

CMD ["python", "app.py"]

