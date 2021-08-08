check
=====

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 check
cp callgraphs/check/buster/0.10.0-3/amd64/check/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
apt source check
cd check-0.10.0
./configure
make
cd tests
cd .libs
LD_LIBRARY_PATH="/home/builder/check-0.10.0/src/.libs:$LD_LIBRARY_PATH"
valgrind --tool=callgrind --callgrind-out-file=check_nofork.txt ./check_nofork
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot check_nofork.txt
dot2fasten check_nofork graph.dot res.json check
cp res.json /callgraphs/check_nofork.json
valgrind --tool=callgrind --callgrind-out-file=check_check_export.txt ./check_check_export
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot check_check_export.txt
dot2fasten check_check_export graph.dot res.json check
cp res.json /callgraphs/check_check_export.json
valgrind --tool=callgrind --callgrind-out-file=check_mem_leaks.txt ./check_mem_leaks
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot check_mem_leaks.txt
dot2fasten check_mem_leaks graph.dot res.json check
cp res.json /callgraphs/check_mem_leaks.json
valgrind --tool=callgrind --callgrind-out-file=check_nofork_teardown.txt ./check_nofork_teardown
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot check_nofork_teardown.txt
dot2fasten check_nofork_teardown graph.dot res.json check
mv res.json /callgraphs/check_nofork_teardown.json
valgrind --tool=callgrind --callgrind-out-file=check_stress.txt ./check_stress
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot check_stress.txt
dot2fasten check_stress graph.dot res.json check
mv res.json /callgraphs/check_stress.json
valgrind --tool=callgrind --callgrind-out-file=check_thread_stress.txt ./check_thread_stress
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot check_thread_stress.txt
dot2fasten check_thread_stress graph.dot res.json check
mv res.json /callgraphs/check_thread_stress.json
exit
cp callgraphs/*.json ./ 

# Integrated
c-integrate stitched.json callback_hang_test.json callback_test.json downsample_test.json float_short_test.json misc_test.json multi_channel_test.json multichan_throughput_test.json reset_test.json simple_test.json snr_bw_test.json termination_test.json throughput_test.json varispeed_test.json integrated.json

rm -rf callgraphs
```
