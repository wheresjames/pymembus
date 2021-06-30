#====================================================================
#
# Examples
#
# Build
# $ docker build -t pymembus .
#
# Run
# $ docker run -it pymembus
#
#====================================================================

FROM ubuntu:20.04 AS pymembus
# FROM debian:10 AS pymembus

# Set timezone
ARG TZ="Europe/Berlin"
ENV TZ $TZ
RUN echo ${TZ} > /etc/timezone

# Automated
ENV DEBIAN_FRONTEND=noninteractive

#--------------------------------------------------------------------
# Copy setup script
COPY ./docker.sh /code/docker.sh
WORKDIR /code

#--------------------------------------------------------------------
# Install Build Dependencies
RUN /code/docker.sh init

#--------------------------------------------------------------------
# If you need a specific version of CMake
# RUN /code/docker.sh cmake 3.20.0

#--------------------------------------------------------------------
# Build the library

# Copy the code
COPY . /code/pymembus
WORKDIR /code/pymembus

# Execute a build
RUN \
       cd /code/pymembus \
    && conan install . \
    && conan build . \
    && cmake --install ./bld

CMD /bin/bash
