FROM alpine:3.14

RUN apk add --update --no-cache openssh sudo python3
RUN ln /usr/bin/python3 /usr/bin/python
EXPOSE 22
COPY files/entrypoint.sh /
COPY files/adduser.sh /
COPY files/deleteuser.sh /
COPY files/sshd_config /etc/ssh/sshd_config
COPY files/banner /etc/motd
RUN chmod 750 / && chown -R root /entrypoint.sh && chown -R root /adduser.sh && chown -R root /deleteuser.sh
ENTRYPOINT ["/entrypoint.sh"]

