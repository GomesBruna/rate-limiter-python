FROM python:3.8.0

WORKDIR '/backend'

RUN pip install redis

RUN pip install threaded

RUN pip install ratelimiter

COPY main.py /backend

CMD ["python3", "main.py"]