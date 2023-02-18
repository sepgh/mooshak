FROM alpine:3.14

RUN apk add --update --no-cache openssh sudo python3
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN ln /usr/bin/python3 /usr/bin/python
EXPOSE 22
COPY files/entrypoint.sh /
COPY files/adduser.sh /
COPY files/deleteuser.sh /
COPY files/sshd_config /etc/sshd/sshd_config
COPY files/banner /etc/motd
ENTRYPOINT ["/entrypoint.sh"]

