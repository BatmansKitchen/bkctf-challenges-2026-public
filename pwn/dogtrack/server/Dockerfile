FROM ubuntu:18.04

RUN apt-get update

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY dogtrack .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .
COPY flag .
COPY ynetd .

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 1337
CMD ["./ynetd", "-p", "1337", "./dogtrack"]