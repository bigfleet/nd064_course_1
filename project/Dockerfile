FROM python:3.10
LABEL maintainer="Jim Van Fleet"

EXPOSE 3111

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && \
      python init_db.py

CMD [ "python", "app.py" ]