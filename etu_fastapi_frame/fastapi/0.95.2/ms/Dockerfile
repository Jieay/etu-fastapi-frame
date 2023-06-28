FROM jieay/python:3.10-slim

# 设置时区为'Asia/Shanghai'
ENV TZ=Asia/Shanghai

# 设置容器的默认时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade --trusted-host mirrors.aliyun.com -i \
    https://mirrors.aliyun.com/pypi/simple/ -r /code/requirements.txt

ENV PYTHONPATH=/code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8052"]
