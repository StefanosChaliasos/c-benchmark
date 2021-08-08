#!/bin/bash
run () {
  d=$1
  old=$(pwd)
  cd $d/.libs
  for i in $(find . -type f -executable -print); do
    valgrind --tool=callgrind --callgrind-out-file=$i.txt ./$i
    gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot $i.txt
    dot2fasten $i graph.dot res.json libgmp
    cp res.json /callgraph/$i.json
  done
  cd $old
}

run ./
run misc
run mpf
run mpn
run mpq
run mpz
run rand
