FROM ubuntu:18.04 

RUN apt-get update
RUN apt-get install -y python3 python3-pip xmlstarlet tidy curl locales

RUN update-locale LANG='sv_SE.UTF-8' LC_CTYPE='sv_SE.UTF-8' LC_NUMERIC='sv_SE.UTF-8' LC_TIME='sv_SE.UTF-8' LC_COLLATE='sv_SE.UTF-8' LC_MONETARY='sv_SE.UTF-8' LC_MESSAGES='sv_SE.UTF-8' LC_PAPER='sv_SE.UTF-8' LC_NAME='sv_SE.UTF-8' LC_ADDRESS='sv_SE.UTF-8' LC_TELEPHONE='sv_SE.UTF-8' LC_MEASUREMENT='sv_SE.UTF-8' LC_IDENTIFICATION='sv_SE.UTF-8' LC_ALL='sv_SE.UTF-8'

RUN pip3 install plumbum

RUN curl --silent --show-error --location 'https://github.com/getzola/zola/releases/download/v0.7.0/zola-v0.7.0-x86_64-unknown-linux-gnu.tar.gz' | tar xzf - -C /usr/local/bin/
