FROM python:3.10.0


WORKDIR /slcm
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /slcm/

RUN python manage.py makemigrations
RUN python manage.py migrate
