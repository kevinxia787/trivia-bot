FROM python:3

ADD bot.py /
ADD trivia.py /
ADD mongodb_util.py /
ADD requirements.txt /

RUN pip install -r ./requirements.txt

CMD ["python", "./bot.py"]

