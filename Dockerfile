FROM debian:stable

ENV dev="git make vim wget python3 python3-pip sudo"

# INSTALL PACKAGES
RUN apt -yqq update && apt -yqq upgrade && apt install -yqq $dev

# INSTALL CScout
WORKDIR /root
RUN git clone https://github.com/dspinellis/cscout.git
WORKDIR cscout
RUN make && make install
WORKDIR /root

COPY ./test-suite .
