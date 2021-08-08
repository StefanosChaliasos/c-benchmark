diffutils
=========

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 diffutils
cp callgraphs/diffutils/buster/1:3.7-3/amd64/diffutils/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
apt source diffutils
cd diffutils-3.7/
./configure
make
cd tests
# In every file change diff command to something like
# valgrind --tool=callgrind --callgrind-out-file=/home/builder/diffutils-3.7/tests/basic.txt diff
# and then execute
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot basic.txt
dot2fasten ../src/diff graph.dot res.json diffutils
cp res.json /callgraphs/basic.json
exit
cp callgraphs/*.json ./ 

# Integrated
c-integrate stitched.json basic.json bignum.json binary.json cmp.json colliding-file-names.json exsess.json filename-quoting.json new-file.json stdin.json integrated.json

rm -rf callgraphs
```
