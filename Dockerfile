FROM python:3.6

ENV FLASK_APP shutify.py
ENV FLASK_CONFIG production

WORKDIR /shutify

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY shutify.py config.py ./


EXPOSE 5000
CMD "gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - shutify:app"