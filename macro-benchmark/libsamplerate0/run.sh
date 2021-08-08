#!/bin/bash

tests="callback_hang_test downsample_test misc_test multichan_throughput_test simple_test termination_test varispeed_test callback_test float_short_test multi_channel_test reset_test snr_bw_test throughput_test"
for t in $tests; do
    valgrind --tool=callgrind --callgrind-out-file=$t.txt ./$t
    gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot $t.txt
    dot2fasten $t graph.dot res.json libsamplerate0
    cp res.json /callgraphs/$t.json
done
