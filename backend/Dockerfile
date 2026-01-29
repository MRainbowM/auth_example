FROM python:3.13

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt --no-cache-dir

