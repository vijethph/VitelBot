FROM python:3.7-slim-buster

# Create app directory
ENV APP_HOME /app
RUN mkdir -pv $APP_HOME
WORKDIR $APP_HOME

ADD . $APP_HOME

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 8443

CMD [ "python", "main.py" ]
