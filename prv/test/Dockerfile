#====================================================================
#
# Build
# $ docker build -t pymembus-test -f ./prv/test/Dockerfile .
#
# Run
# $ docker run -it pymembus-test
#
# Cleanup docker
# $ docker system prune -f
#
#====================================================================

# FROM ubuntu:20.04 AS pymembus
FROM debian:11 AS pymembus

# Set timezone
ARG TZ="Europe/Berlin"
ENV TZ $TZ
RUN echo ${TZ} > /etc/timezone

# Automated
ENV DEBIAN_FRONTEND=noninteractive

#--------------------------------------------------------------------
# Install Build Dependencies
RUN \
       apt-get -yq update \
    && apt-get -yq install wget build-essential libboost-all-dev \
                           nano git cmake doxygen graphviz \
                           go-md2man ronn

# Install a web browser to view help file (pymembus help)
# RUN apt-get -yq install lynx


#--------------------------------------------------------------------
# Copy setup script
COPY . /code/pymembus
WORKDIR /code

ENV DOCKERSCRIPT /code/pymembus/prv/test/docker.sh

#--------------------------------------------------------------------
# Ensure we have a minimum cmake version
RUN ${DOCKERSCRIPT} check-cmake "3.15" "release"

#--------------------------------------------------------------------
# CMake build
RUN ${DOCKERSCRIPT} test-cmake

#--------------------------------------------------------------------
# pip build
RUN ${DOCKERSCRIPT} test-pip


CMD /bin/bash
