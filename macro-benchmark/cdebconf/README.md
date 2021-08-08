cdebconf
========

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 cdebconf
cp callgraphs/cdebconf/buster/0.249/amd64/cdebconf/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
docker run -it --rm -v $(pwd)/callgraphs:/callgraphs dynamic /bin/bash
sudo apt install  adwaita-icon-theme autoconf automake autopoint autotools-dev bsdmainutils \
  ca-certificates debhelper dh-autoreconf dh-exec dh-strip-nondeterminism dwz \
  file fontconfig fontconfig-config fonts-dejavu-core gettext gettext-base \
  gir1.2-atk-1.0 gir1.2-freedesktop gir1.2-gdkpixbuf-2.0 gir1.2-glib-2.0 \
  gir1.2-gtk-2.0 gir1.2-harfbuzz-0.0 gir1.2-pango-1.0 groff-base \
  gtk-update-icon-cache hicolor-icon-theme icu-devtools intltool-debian \
  libarchive-zip-perl libatk1.0-0 libatk1.0-data libatk1.0-dev \
  libavahi-client3 libavahi-common-data libavahi-common3 libblkid-dev libbsd0 \
  libcairo-gobject2 libcairo-script-interpreter2 libcairo2 libcairo2-dev \
  libcroco3 libcups2 libdatrie1 libdbus-1-3 libdebian-installer-extra4 \
  libdebian-installer4 libdebian-installer4-dev libelf1 libexpat1 \
  libexpat1-dev libffi-dev libfile-stripnondeterminism-perl libfontconfig1 \
  libfontconfig1-dev libfreetype6 libfreetype6-dev libfribidi-dev libfribidi0 \
  libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-bin libgdk-pixbuf2.0-common \
  libgdk-pixbuf2.0-dev libgirepository-1.0-1 libglib2.0-0 libglib2.0-bin \
  libglib2.0-data libglib2.0-dev libglib2.0-dev-bin libgpm2 libgraphite2-3 \
  libgraphite2-dev libgssapi-krb5-2 libgtk2.0-0 libgtk2.0-common libgtk2.0-dev \
  libharfbuzz-dev libharfbuzz-gobject0 libharfbuzz-icu0 libharfbuzz0b \
  libice-dev libice6 libicu-dev libicu63 libjbig0 libjpeg62-turbo libk5crypto3 \
  libkeyutils1 libkrb5-3 libkrb5support0 liblzo2-2 libmagic-mgc libmagic1 \
  libmount-dev libmpdec2 libncurses6 libnewt-dev libnewt0.52 libpango-1.0-0 \
  libpango1.0-dev libpangocairo-1.0-0 libpangoft2-1.0-0 libpangoxft-1.0-0 \
  libpcre16-3 libpcre3-dev libpcre32-3 libpcrecpp0v5 libpipeline1 \
  libpixman-1-0 libpixman-1-dev libpng-dev libpng16-16 libpthread-stubs0-dev \
  libpython3-stdlib libpython3.7-minimal libpython3.7-stdlib librsvg2-2 \
  librsvg2-common libselinux1-dev libsepol1-dev libsigsegv2 libslang2 \
  libslang2-dev libsm-dev libsm6 libssl1.1 libtextwrap-dev libtextwrap1 \
  libthai-data libthai0 libtiff5 libtool libuchardet0 libwebp6 libx11-6 \ 
  libx11-data libx11-dev libxau-dev libxau6 libxcb-render0 libxcb-render0-dev \
  libxcb-shm0 libxcb-shm0-dev libxcb1 libxcb1-dev libxcomposite-dev \
  libxcomposite1 libxcursor-dev libxcursor1 libxdamage-dev libxdamage1 \
  libxdmcp-dev libxdmcp6 libxext-dev libxext6 libxfixes-dev libxfixes3 \
  libxft-dev libxft2 libxi-dev libxi6 libxinerama-dev libxinerama1 libxml2 \
  libxml2-utils libxrandr-dev libxrandr2 libxrender-dev libxrender1 m4 man-db \
  mime-support openssl pango1.0-tools pkg-config po-debconf python-pip-whl \
  python3 python3-distutils python3-lib2to3 python3-minimal python3-pip \
  python3.7 python3.7-minimal sensible-utils \
  shared-mime-info time ucf uuid-dev vim vim-common vim-runtime x11-common \
  x11proto-composite-dev x11proto-core-dev x11proto-damage-dev x11proto-dev \
  x11proto-fixes-dev x11proto-input-dev x11proto-randr-dev x11proto-xext-dev \
  x11proto-xinerama-dev xorg-sgml-doctools xtrans-dev xxd zlib1g-dev
apt source cdebconf
cd cdebconf-0.249/
autoreconf -f -i
./configure
make
./configure --with-frontend=text --with-conffile=./cdebconf.conf
make
cd src/test
cp ../cdebconf.conf ./
valgrind --tool=callgrind --callgrind-out-file=debconf.txt ../debconf test.config
gprof2dot -f callgrind -n 0.0 -e 0.0 -o graph.dot debconf.txt
dot2fasten ../debconf graph.dot res.json cdebconf
cp res.json /callgraphs/debconf.json
exit
cp callgraphs/debconf.json ./

# Integrated
c-integrate stitched.json debconf.json integrated.json

rm -rf callgraphs
```
