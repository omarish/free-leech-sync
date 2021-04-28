FROM python:3.9

WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "sync", "600"]