FROM python:3.10.14

WORKDIR /app
ADD . /app

RUN rm ./config.yml
RUN mv live_config.yml ./config.yml

RUN apt-get update && apt-get install -y python3-dev gcc  # 能够编译Rust代码并使用二进制文件

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 5002
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5002", "app:app"]
# 四个worker，监听5002端口，app:app是启动的Flask应用，表示应用程序在app.py文件中，应用程序是变量名app下的Flask实例