FROM ubuntu:20.04

RUN apt-get update

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY igetsit .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .
COPY flag .
COPY ynetd .

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 5377
CMD ["./ynetd", "-p", "5377", "./igetsit"]
