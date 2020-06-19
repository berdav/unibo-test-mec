FROM debian

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-flask
RUN apt-get install -y python3-requests

COPY app.py /usr/local/bin/app.py
COPY app_site /var/www/
RUN chmod +x /usr/local/bin/app.py

CMD /usr/local/bin/app.py
