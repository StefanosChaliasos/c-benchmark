fdupes
======

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 fdupes
cp callgraphs/fdupes/buster/1:1.6.1-2/amd64/fdupes/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
sudo apt install autoconf automake autopoint autotools-dev bsdmainutils ca-certificates \
  debhelper dh-autoreconf dh-exec dh-strip-nondeterminism dwz file gettext \
  gettext-base groff-base intltool-debian libarchive-zip-perl libbsd0 \
  libcroco3 libelf1 libexpat1 libfile-stripnondeterminism-perl libglib2.0-0 \
  libgpm2 libicu63 libmagic-mgc libmagic1 libmpdec2 libncurses6 libpipeline1 \
  libpython3-stdlib libpython3.7-minimal libpython3.7-stdlib libsigsegv2 \
  libssl1.1 libtool libuchardet0 libxml2 m4 man-db mime-support openssl \
  po-debconf python-pip-whl python3 python3-distutils python3-lib2to3 \
  python3-minimal python3-pip python3.7 python3.7-minimal \
  sensible-utils time vim vim-common \
  vim-runtime xxd
apt source fdupes
cd fdupes-1.6.1/
make
valgrind --tool=callgrind --callgrind-out-file=test1.txt ./fdupes testdir/
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot test1.txt
dot2fasten fdupes graph.dot res.json fdupes
cp res.json /callgraphs/test1.json
valgrind --tool=callgrind --callgrind-out-file=test2.txt ./fdupes -r testdir/
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot test2.txt
dot2fasten fdupes graph.dot res.json fdupes
cp res.json /callgraphs/test2.json
exit
cp callgraphs/*.json ./

# Integrated
c-integrate stitched.json test1.json test2.json integrated.json

rm -rf callgraphs
```
