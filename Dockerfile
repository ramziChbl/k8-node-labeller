FROM python:alpine

RUN pip install kubernetes

COPY app.py /app.py

RUN chmod u+x /app.py

ENTRYPOINT ["/app.py"]
