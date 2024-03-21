FROM python:3.10

WORKDIR /rbpo

COPY . /rbpo
RUN pip3 install -r requirements.txt

CMD ["python3","-u", "test_bot.py"]
