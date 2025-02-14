FROM python:3.9.20-slim

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR  /src

COPY requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt

COPY src/ /src/
RUN ls -la /src/*

CMD ["python3", "/src/main.py"]

