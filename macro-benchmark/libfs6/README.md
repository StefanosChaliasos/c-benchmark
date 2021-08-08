libfs6
======

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 libfs
cp callgraphs/libfs/buster/2:1.0.7-1/amd64/libfs6/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
sudo apt install  autoconf automake autopoint autotools-dev bsdmainutils ca-certificates \
  debhelper dh-autoreconf dh-exec dh-strip-nondeterminism dwz file gettext \
  gettext-base groff-base intltool-debian libarchive-zip-perl libbsd0 \
  libcroco3 libelf1 libexpat1 libfile-stripnondeterminism-perl libglib2.0-0 \
  libgpm2 libicu63 libmagic-mgc libmagic1 libmpdec2 libncurses6 libpipeline1 \
  libpython3-stdlib libpython3.7-minimal libpython3.7-stdlib libsigsegv2 \
  libssl1.1 libtool libuchardet0 libxml2 m4 man-db mime-support openssl \
  pkg-config po-debconf python-pip-whl python3 python3-distutils \
  python3-lib2to3 python3-minimal python3-pip python3.7 python3.7-minimal \
  sensible-utils time vim vim-common \
  vim-runtime x11proto-core-dev x11proto-dev xorg-sgml-doctools xtrans-dev \
  xutils-dev xxd libfs6
apt source libfs
cd libfs-1.0.7/
./configure
make 
LD_LIBRARY_PATH="/home/builder/libfs-1.0.7/src/.libs:$LD_LIBRARY_PATH"
cd test
make
cd .libs
valgrind --tool=callgrind --callgrind-out-file=test.txt ./FSGetErrorText
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot test.txt
dot2fasten FSGetErrorText graph.dot res.json libfs6
cp res.json /callgraphs/res.json
exit
cp callgraphs/res.json ./

# Integrated
c-integrate stitched.json res.json integrated.json

rm -rf callgraphs
```
