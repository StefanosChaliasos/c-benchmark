zlib1g-dev
==========

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 zlib
cp callgraphs/zlib/buster/1:1.2.11.dfsg-1/amd64/zlib1g-dev/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraph dynamic /bin/bash
apt source zlib
cd zlib-1.2.11.dfsg
./configure && make
echo hello world | valgrind --tool=callgrind --callgrind-out-file=minigzip.txt ./minigzip
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot minigzip.txt
dot2fasten minigzip graph.dot res.json zlib1g-dev
cp res.json /callgraph/minigzip.json
echo hello world | valgrind --tool=callgrind --callgrind-out-file=minigzipsh.txt ./minigzipsh
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot minigzipsh.txt
dot2fasten minigzipsh graph.dot res.json zlib1g-dev
cp res.json /callgraph/minigzipsh.json
exit
cp callgraphs/minigzip.json ./ 
cp callgraphs/minigzipsh.json ./ 

# Integrated
c-integrate stitched.json minigzip.json minigzipsh.json integrated.json

rm -rf callgraphs
```
