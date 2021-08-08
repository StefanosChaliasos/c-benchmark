libsamplerate0
==============

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 libsamplerate
cp callgraphs/libsamplerate/buster/0.1.9-2/amd64/libsamplerate0 fcg.json
c-stitch fcg.json -o stitched.json -k

# Dynamic
cp run.sh callgraphs
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
apt source libsamplerate
cd libsamplerate-0.1.9
sudo apt install autoconf automake autopoint autotools-dev bsdmainutils ca-certificates debhelper dh-autoreconf dh-exec dh-strip-nondeterminism dwz file gettext gettext-base groff-base intltool-debian libarchive-zip-perl libbsd0 libcroco3 libelf1 libexpat1 libfftw3-bin libfftw3-dev libfftw3-double3 libfftw3-long3 libfftw3-quad3 libfftw3-single3 libfile-stripnondeterminism-perl libflac-dev libflac8 libglib2.0-0 libgpm2 libicu63 libmagic-mgc libmagic1 libmpdec2 libncurses6 libogg-dev libogg0 libpipeline1 libpython3-stdlib libpython3.7-minimal libpython3.7-stdlib libsigsegv2 libsndfile1 libsndfile1-dev libssl1.1 libtool libuchardet0 libvorbis-dev libvorbis0a libvorbisenc2 libvorbisfile3 libxml2 m4 man-db mime-support openssl pkg-config po-debconf python-pip-whl python3 python3-distutils python3-lib2to3 python3-minimal python3-pip python3.7 python3.7-minimal sensible-utils time vim vim-common vim-runtime xxd libsamplerate0-dev
./configure
make
cd tests
cd .libs
#1
mv /callgraphs/run.sh ./
./run.sh

exit
cp callgraphs/*.json ./ 

# Integrated
c-integrate stitched.json callback_hang_test.json callback_test.json downsample_test.json float_short_test.json misc_test.json multi_channel_test.json multichan_throughput_test.json reset_test.json simple_test.json snr_bw_test.json termination_test.json throughput_test.json varispeed_test.json integrated.json

rm -rf callgraphs
```
