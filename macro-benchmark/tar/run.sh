#!/bin/bash

for t in $(ls *.txt); do
    gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot $t
    dot2fasten ../src/tar graph.dot res.json tar
    cp res.json /callgraphs/$t.json
done
