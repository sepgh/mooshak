FROM alpine:3.14

RUN apk add --update --no-cache wget
WORKDIR /
RUN wget https://github.com/erebe/wstunnel/releases/download/v5.1/wstunnel-linux-x64
RUN chmod +x wstunnel-linux-x64
EXPOSE 80
ENTRYPOINT ["/bin/sh", "-c", "/wstunnel-linux-x64 --server ws://0.0.0.0:80 -r mooshak:22"]

