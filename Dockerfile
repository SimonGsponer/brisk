FROM registry.access.redhat.com/ubi8/python-39:1-48

COPY . .

RUN ["pip3", "install", "-r", "requirements.txt"]

CMD ["python3", "-m", "src.main"]
