FROM python:3.7.6
ENV PYTHONPATH /
COPY ./requirements.txt /requirements.txt
COPY ./handler.py /handler.py
RUN pip install -r /requirements.txt
RUN mkdir -p /etc/slacker
CMD ["aiosmtpd", "-n", "-l", "0.0.0.0:25", "-c", "/handler.MessageHandler"]
EXPOSE 8025
