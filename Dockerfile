# For more information, please refer to https://aka.ms/vscode-docker-python
FROM tensorflow/tensorflow:latest-gpu

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# ensure pip is up to date
RUN pip install --upgrade pip

# install opencv dependencies
# Needed to add key update since it vanished recently?
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC && \
    apt-get update && \
    apt-get install -y \
      libsm6 libxext6 libxrender-dev \
      libv4l-dev libgl1-mesa-dev \
      cmake

  # Cmake is needed for dlib -> face_recognition

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app && \
    groupmod -g 986 video && \
    usermod -a -G video appuser

USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "fakecam/fake.py"]
# ENTRYPOINT ls -la /app/
