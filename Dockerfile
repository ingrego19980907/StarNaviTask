FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN pip install --upgrade pip
COPY /src/requirements.txt /code/
RUN python -m pip install -r requirements.txt
COPY .env /code/
COPY ./src /code/



