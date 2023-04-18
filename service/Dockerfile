FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=TRUE

ENV APP_HOME=/var/www/html/service
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# 将当前目录加入到工作目录中（. 表示当前目录）
ADD . $APP_HOME

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN sed -i 's/\r//' ./start.sh

RUN chmod +x ./start.sh

RUN sed -i 's/\r//' ./start_celery.sh

RUN chmod +x ./start_celery.sh

RUN sed -i 's/\r//' ./start_flower.sh

RUN chmod +x ./start_flower.sh

ENTRYPOINT /bin/bash ./start.sh

