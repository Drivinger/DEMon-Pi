##base image
FROM rpiguru/docker-python3-opencv-arm:armv7hf-latest
# install required packages
RUN apt-get update -y && apt-get install -y libsm6 libxext6 libxrender-dev ffmpeg
RUN pip3 install --upgrade pip

WORKDIR /app

## copy requirements and install packages
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

## copy the source code and configs
COPY ./iWebLens_server.py iWebLens_server.py
COPY ./yolo_tiny_configs/ yolo_tiny_configs/

## FLASK runs on defualt 5000, expose this port
EXPOSE 5000
# app and arguments
ENTRYPOINT [ "python3" ]
CMD [ "iWebLens_server.py", "./yolo_tiny_configs" ]
