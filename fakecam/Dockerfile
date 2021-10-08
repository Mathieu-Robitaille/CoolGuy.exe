# Base image with TensorFlow GPU requirements
FROM tensorflow/tensorflow:latest-gpu

# ensure pip is up to date
RUN pip install --upgrade pip

# install opencv dependencies
RUN apt-get update && \
    apt-get install -y \
      libsm6 libxext6 libxrender-dev \
      libv4l-dev libgl1-mesa-dev

# install our requirements
WORKDIR /src
COPY requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt

# run our fake camera script (with unbuffered output for easier debug)
COPY *.py /src/
ENTRYPOINT python -u fake.py