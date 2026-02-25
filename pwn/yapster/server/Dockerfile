FROM ubuntu:20.04

RUN apt-get update

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY yapster .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .
COPY flag .
COPY ynetd .

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 1111
CMD ["./ynetd", "-p", "1111", "./yapster"]
