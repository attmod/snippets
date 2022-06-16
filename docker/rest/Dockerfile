ARG DOCKER_SRC

FROM $DOCKER_SRC

USER root
RUN adduser docky rdma

RUN pip3 install flask

USER docky
