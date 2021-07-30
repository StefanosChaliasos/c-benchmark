FROM debian:stable

ENV dev="git make vim wget python3 python3-pip sudo"
ENV val="graphviz libgraphviz-dev valgrind binutils"
ENV pip_deps="pandas networkx pydot gprof2dot setuptools pygraphviz"

# INSTALL PACKAGES
RUN apt -yqq update && apt -yqq upgrade && apt install -yqq $dev $val
RUN pip3 install $pip_deps

# INSTALL CScout
WORKDIR /root
RUN git clone https://github.com/dspinellis/cscout.git
WORKDIR cscout
RUN make && make install
WORKDIR /root

RUN wget https://raw.githubusercontent.com/fasten-project/c-integrate/master/c-integrate
RUN mv ./c-integrate /usr/local/bin/
RUN chmod +x /usr/local/bin/c-integrate

RUN wget https://raw.githubusercontent.com/fasten-project/debian-builder/master/dynamic/dot2fasten
RUN mv ./dot2fasten /usr/local/bin/
RUN chmod +x /usr/local/bin/dot2fasten

COPY ./test-suite /root/test-suite
COPY ./convert_cscout_to_stiched /usr/local/bin/convert_cscout_to_stiched
RUN chmod +x /usr/local/bin/convert_cscout_to_stiched

USER root
WORKDIR /root/test-suite
