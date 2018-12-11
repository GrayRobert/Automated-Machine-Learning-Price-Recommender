FROM grayrobert/price-recommender-base:latest
MAINTAINER Robert Gray <grayarobert@gmail.com>

# Install dev/build dependencies
RUN apt-get update && \
    apt-get install -qy python3-dev && \
    apt-get install build-essential swig

# Activate virtual environment and install wheel support
RUN . /venv/bin/activate && \
    pip3 install wheel --upgrade

# PIP environment variables (NOTE: must be set after installing wheel)
ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache

ENV PYTHONUNBUFFERED 1

# OUTPUT: Build artefacts (Wheels) are output here
VOLUME /wheelhouse

# OUTPUT: Build cache
VOLUME /build

# Add test entrypoint script
COPY scripts/production_entrypoint.sh /usr/local/bin/production_entrypoint.sh
RUN chmod +x /usr/local/bin/production_entrypoint.sh

# Set defaults for entrypoint and command string
ENTRYPOINT ["production_entrypoint.sh"]

# Add application source
COPY rest-api /app

WORKDIR /app
RUN chmod +x manage.py

RUN rm /app/recommender/services/train.py
RUN mv /app/recommender/services/train.production.py /app/recommender/services/train.py

