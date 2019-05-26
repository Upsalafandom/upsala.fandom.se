FROM ubuntu:18.04 

RUN apt-get update
RUN apt-get install -y curl language-pack-sv python3 python3-pip tidy xmlstarlet

RUN pip3 install plumbum

RUN curl --silent --show-error --location 'https://github.com/getzola/zola/releases/download/v0.7.0/zola-v0.7.0-x86_64-unknown-linux-gnu.tar.gz' | tar xzf - -C /usr/local/bin/
