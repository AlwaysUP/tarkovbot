FROM python:3.7-alpine
WORKDIR /usr/local/bin
COPY requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add curl curl-dev bash
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3","bot.py"]