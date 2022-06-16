FROM python:3.9

RUN pip install -r requirements.txt

RUN mkdir -p /workdir
WORKDIR /workdir
ADD . /workdir/

EXPOSE 8080
CMD ["python3", "/workdir/example.py"]
