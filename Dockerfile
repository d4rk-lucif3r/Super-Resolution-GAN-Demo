FROM jjanzic/docker-python3-opencv:opencv-4.0.0
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY ./requirements.txt /tmp/
RUN pip install -U pip && pip install -r /tmp/requirements.txt
COPY . ./app
WORKDIR app
ENTRYPOINT python app.py