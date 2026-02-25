FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
       git \
       python3 \
       xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 ctf
USER ctf
WORKDIR /home/ctf

ENV PATH="/home/ctf/.elan/bin:${PATH}"
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf \
    | sh -s -- -y --default-toolchain none

WORKDIR /home/ctf/app
COPY --chown=ctf:ctf challenge ./challenge
COPY --chown=ctf:ctf server ./server

RUN cd challenge && lake build

EXPOSE 5000

ENV MAX_CONNECTIONS=100
ENV PORT=5000
ENV FLAG=bkctf{lmk-in-a-ticket-if-you-do-this-without-native_decide}

ENTRYPOINT ["python3", "server/main.py"]
