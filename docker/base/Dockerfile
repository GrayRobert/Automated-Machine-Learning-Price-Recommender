FROM ubuntu:18.04
MAINTAINER Robert Gray <grayarobert@gmail.com>

# Prevent dpkg errors
ENV TERM=xterm-256color

# Install Python runtime
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

# Create virtual environment
# Upgrade PIP in virtual environment to latest version
RUN pip3 install virtualenv && \
    virtualenv /venv && \
    . /venv/bin/activate

# Add entrypoint script
ADD scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

LABEL application=price-recommender-server

