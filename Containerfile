FROM registry.fedoraproject.org/fedora:38

RUN dnf -y install openssl1.1 just xmlstarlet tidy hut git

RUN curl -sSL https://github.com/getzola/zola/releases/download/v0.9.0/zola-v0.9.0-x86_64-unknown-linux-gnu.tar.gz | tar -C /usr/local/bin -zx
