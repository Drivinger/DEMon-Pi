##base image
FROM jjanzic/docker-python3-opencv@sha256:4d62a19be279775d9b8938cd097530e1b7102ce50445df0b26d19590a9fea90b
# install required packages
RUN apt-get update -y && apt-get install -y libsm6 libxext6 libxrender-dev ffmpeg
WORKDIR /app
## copy requirements and install packages
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
## copy the source code and configs
COPY iWebLens_server.py /app
COPY yolo_tiny_configs/ /app/yolo_tiny_configs/
## FLASK runs on defualt 5000, expose this port
EXPOSE 5000
# app and arguments
ENTRYPOINT [ "python3" ]
CMD [ "iWebLens_server.py", "./yolo_tiny_configs" ]
