libdebian-installer4
====================

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 libdebian-installer
cp callgraphs/libdebian-installer/buster/0.119/amd64/libdebian-installer4/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
sudo apt install  autoconf automake autopoint autotools-dev bsdmainutils ca-certificates check \
  debhelper dh-autoreconf dh-exec dh-strip-nondeterminism doxygen dwz file \
  gettext gettext-base groff-base intltool-debian libarchive-zip-perl libbsd0 \
  libclang1-6.0 libcroco3 libedit2 libelf1 libexpat1 \
  libfile-stripnondeterminism-perl libglib2.0-0 libgpm2 libicu63 libllvm6.0 \
  libmagic-mgc libmagic1 libmpdec2 libncurses6 libpipeline1 libpython3-stdlib \
  libpython3.7-minimal libpython3.7-stdlib libsigsegv2 libssl1.1 \
  libsubunit-dev libsubunit0 libtool libuchardet0 libxapian30 libxml2 m4 \
  man-db mime-support openssl pkg-config po-debconf python-pip-whl python3 \
  python3-distutils python3-lib2to3 python3-minimal python3-pip python3.7 \
  python3.7-minimal sensible-utils time vim \
  vim-common vim-runtime xxd
apt source libdebian-installer
cd libdebian-installer-0.119/
autoreconf -f -i
./configure
make
cd test
make check
cd .libs
valgrind --tool=callgrind --callgrind-out-file=test.txt ./test
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot test.txt
dot2fasten test graph.dot res.json libdebian-installer4
cp res.json /callgraphs/
exit
cp callgraphs/res.json ./

# Integrated
c-integrate stitched.json res.json integrated.json

rm -rf callgraphs
```
