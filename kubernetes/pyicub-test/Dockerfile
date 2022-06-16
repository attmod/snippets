ARG DOCKER_SRC

FROM $DOCKER_SRC

USER root

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install flask kafka-python numpy Pillow

RUN useradd -ms /bin/bash docky

RUN mkdir -p /workdir && chmod 777 /workdir
USER docky
