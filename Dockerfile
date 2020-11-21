FROM python:3.8-slim-buster

WORKDIR /var/www/app

# create .venv dir (this is where pipenv will install)
RUN mkdir .venv

# install dep
RUN pip install --upgrade pip
RUN pip install pipenv
RUN apt-get update && apt-get install iproute2 tzdata -y

COPY . /var/www/app

RUN pipenv install --deploy

EXPOSE 5000

# timezone default
ENV TZ Europe/Stockholm

CMD [ "/var/www/app/entrypoint.sh" ]
