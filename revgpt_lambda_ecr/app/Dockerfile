ARG FUNCTION_DIR=/root/function
FROM continuumio/anaconda3 as build-image
RUN apt-get update
RUN apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates vim htop
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  autoconf \
  libtool \
  libcurl4-openssl-dev


ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}
COPY app/* ${FUNCTION_DIR}

RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

FROM continuumio/anaconda3
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
RUN apt-get update
RUN apt-get -y install curl vim
COPY app/* /opt/conda/lib/python3.9/site-packages/
RUN chmod -R 777 /root
RUN pip install awslambdaric openai
