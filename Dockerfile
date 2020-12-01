FROM python:3.9-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
ADD requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
      && python -m pip install -r requirements.txt \
      && apk del .build-deps gcc musl-dev

WORKDIR /app
ADD . /app

RUN adduser -S appuser && chown -R appuser /app
USER appuser

CMD ["python", "lyna.py"]
