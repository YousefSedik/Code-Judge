# setup server

# 1: start docker kernel + python
FROM python:3.11-slim

# 2: ENV: show logs
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# 3: update kernel + install dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev  bubblewrap postgresql  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



# 4: create project folder: kernel
WORKDIR /app

# 5: Copy requirements
COPY requirements.txt /app/requirements.txt

# 6: install requirements
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# 7: copy project code --> docker
COPY . /app/

EXPOSE 8000