FROM ubuntu:18.04
MAINTAINER Robert Gray <grayarobert@gmail.com>

# Prevent dpkg errors
ENV TERM=xterm-256color

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Install Python runtime
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && apt-get install -y curl \
    && apt-get -y autoclean

# Create virtual environment
RUN pip3 install virtualenv && \
    virtualenv /venv && \
    . /venv/bin/activate

# Create NVM directory
RUN mkdir /usr/local/nvm

# nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 10.14.1

# install nvm
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Add entrypoint script
ADD scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

LABEL application=price-recommender-server

