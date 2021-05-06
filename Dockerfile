FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Requirements
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pyqt5 \
    build-essential \
    python3-dev \
    python3-pip 

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY /media /media
COPY /results /results
COPY /files /files
COPY /times /times

COPY segmentation.py /tmp/segmentation.py

ENTRYPOINT ["/bin/bash", "-c", "python3 /tmp/segmentation.py > /times/times.csv"]
