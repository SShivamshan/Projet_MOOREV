FROM ubuntu:20.04 as base

ENV DEBIAN_FRONTEND noninteractive

ARG USERNAME=viameuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
# Install necessary tools and libraries
RUN apt-get update && \
    apt-get install -y libgl1-mesa-dri libgl1-mesa-glx mesa-utils libglib2.0-0 libsensors-dev libnspr4 libnss3 libatk1.0-0 libx11-dev libx11-xcb-dev libatk-bridge2.0-0 libdbus-1-dev libgtk-3-0 libpangocairo-1.0-0 libcairo2-dev libxcomposite-dev libxdamage1 libxtst6 libxfixes-dev libxrandr2 libexpat1 libdrm-dev libxkbcommon-x11-0 libgbm-dev libasound2 libcups2 libcanberra-gtk-module libcanberra-gtk3-module && \
    apt-get install -y gnupg wget apt-transport-https software-properties-common && \
    wget -q https://xpra.org/gpg.asc -O- | apt-key add - && \
    add-apt-repository "deb https://xpra.org/ focal main" && \
    apt-get update && \
    apt-get install -y xpra xterm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Copy and extract installation files
ADD ../docker/VIAME-v0.20.3-Linux-64Bit.tar.gz /Downloads/

# Set the working directory
WORKDIR /Downloads

# Create installation directory
RUN mkdir -p /opt/noaa/
RUN mv viame /opt/noaa

USER root
# Had to give permission if not launched an error
RUN chown root:root /opt/noaa/viame/dive/chrome-sandbox && \
    chmod 4755 /opt/noaa/viame/dive/chrome-sandbox

# TO retrieve the downloaded data
RUN mkdir /home/viameuser/exports
RUN chmod +w /home/viameuser/exports/
# VOLUME /home/viameuser/exports
RUN chown viameuser:viameuser /home/viameuser/exports/

# USER since ./launch_dive_interface.sh doesn't launch from root
USER viameuser
ENV XDG_RUNTIME_DIR=/tmp

EXPOSE 9876
WORKDIR /opt/noaa/viame

CMD ["bash", "-c", "xpra start --bind-tcp=0.0.0.0:9876 --start=./launch_dive_interface.sh --daemon=no --exit-with-client --opengl=yes"]

# Commande to run the docker : sudo docker run -p 9876:9876 --gpus all -it --name page_web -e DISPLAY=:1 --security-opt seccomp=docker/chrome.json -e ELECTRON_ENABLE_LOGGING=true -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority moorev/viame
