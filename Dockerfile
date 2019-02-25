FROM amd64/python:3.7.2-alpine

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /entrypoint /app/

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt

COPY docupdater /app/docupdater

RUN pip install --no-cache-dir .

ENTRYPOINT ["entrypoint"]