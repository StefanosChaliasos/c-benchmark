tar
=========

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 tar
cp callgraphs/tar/buster/1.30+dfsg-6/amd64/tar/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
cp run.sh callgraphs
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
sudo apt install autoconf automake autopoint autotools-dev bsdmainutils ca-certificates \
  debhelper dh-autoreconf dh-exec dh-strip-nondeterminism dwz file gettext \
  gettext-base groff-base intltool-debian libacl1-dev libarchive-zip-perl \
  libattr1-dev libbsd0 libcroco3 libelf1 libexpat1 \
  libfile-stripnondeterminism-perl libglib2.0-0 libgpm2 libicu63 libmagic-mgc \
  libmagic1 libmpdec2 libncurses6 libpcre16-3 libpcre3-dev libpcre32-3 \
  libpcrecpp0v5 libpipeline1 libpython3-stdlib libpython3.7-minimal \
  libpython3.7-stdlib libselinux1-dev libsepol1-dev libsigsegv2 libssl1.1 \
  libtool libuchardet0 libxml2 m4 man-db mime-support openssl po-debconf \
  python-pip-whl python3 python3-distutils python3-lib2to3 python3-minimal \
  python3-pip python3.7 python3.7-minimal  \
  sensible-utils time vim vim-common vim-runtime xxd
apt source tar
cd tar-1.30+dfsg/
autoreconf -f -i
./configure
make
cd tests
# Update testsuite to add the following command before tar executions
# valgrind --tool=callgrind --callgrind-out-file=/home/builder/tar-1.30+dfsg/tests/1.txt
make check
cp /callgraphs/run.sh ./
./run.sh
exit
cp callgraphs/*.json ./ 

c-integrate stitched.json 10.txt.json   19.txt.json   2c.txt.json   33.txt.json   40.txt.json   45.txt.json   7.txt.json    12.txt.json   20.txt.json   2d.txt.json   38.txt.json   41.txt.json   4b.txt.json   8.txt.json    13.txt.json   26.txt.json   30.txt.json   3b.txt.json   42.txt.json   5b.txt.json   9.txt.json 18.txt.json   27.txt.json   31.txt.json   4.txt.json    43.txt.json   6b.txt.json integrated.json

rm -rf callgraphs
```
