libgmp
======

```bash
mkdir callgraphs

# Static
docker run -it --rm --privileged -v $(pwd)/callgraphs:/callgraphs \
    sbuild-cscout sbuild --apt-update --no-apt-upgrade \
    --no-apt-distupgrade --batch --stats-dir=/var/log/sbuild/stats \
    --dist=buster --arch=amd64 gmp
cp callgraphs/zlib/buster/1:1.2.11.dfsg-1/amd64/zlib1g-dev/fcg.json ./
c-stitch fcg.json -o stitched.json -k

# Dynamic
cp run.sh callgraphs
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
  sbuild-build-depends-main-dummy time vim vim-common \
  vim-runtime xxd
apt source gmp
cd gmp-6.1.2+dfsg/
./configure
make
cd tests
make check
cp /callgraphs/run.sh ./
./run.sh
exit

# Integrated
c-integrate stitched.json bit.json convert.json dive.json dive_ui.json io.json logic.json reuse.json t-add.json t-addsub.json t-aors.json t-aors_1.json t-aorsmul.json t-asmtype.json t-bdiv.json t-bin.json t-broot.json t-brootinv.json t-bswap.json t-cdiv_ui.json t-cmp.json t-cmp_d.json t-cmp_si.json t-cmp_ui.json t-cmp_z.json t-cong.json t-cong_2exp.json t-constants.json t-conv.json t-count_zeros.json t-div.json t-div_2exp.json t-divis.json t-divis_2exp.json t-divrem_1.json t-dm2exp.json t-eq.json t-equal.json t-export.json t-fac_ui.json t-fat.json t-fdiv.json t-fdiv_ui.json t-fib_ui.json t-fits.json t-gcd.json t-gcd_ui.json t-get_d.json t-get_d_2exp.json t-get_si.json t-get_str.json t-get_ui.json t-gsprec.json t-hamdist.json t-hgcd.json t-hgcd_appr.json t-hightomask.json t-import.json t-inp_str.json t-instrument.json t-int_p.json t-inv.json t-invert.json t-io_raw.json t-iord_u.json t-iset.json t-jac.json t-lc2exp.json t-lcm.json t-limbs.json t-locale.json t-lucnum_ui.json t-matrix22.json t-md_2exp.json t-mfac_uiui.json t-minvert.json t-mod_1.json t-modlinv.json t-mp_bases.json t-mt.json t-mul.json t-mul_i.json t-mul_ui.json t-muldiv.json t-mullo.json t-mulmid.json t-mulmod_bnm1.json t-nextprime.json t-oddeven.json t-parity.json t-perfpow.json t-perfsqr.json t-popc.json t-popcount.json t-pow.json t-pow_ui.json t-powm.json t-powm_ui.json t-pprime_p.json t-primorial_ui.json t-printf.json t-rand.json t-remove.json t-root.json t-scan.json t-scanf.json t-set.json t-set_d.json t-set_f.json t-set_q.json t-set_si.json t-set_str.json t-set_ui.json t-sizeinbase.json t-sqrlo.json t-sqrmod_bnm1.json t-sqrt.json t-sqrt_ui.json t-sqrtrem.json t-sub.json t-tdiv.json t-tdiv_ui.json t-toom2-sqr.json t-toom22.json t-toom3-sqr.json t-toom32.json t-toom33.json t-toom4-sqr.json t-toom42.json t-toom43.json t-toom44.json t-toom52.json t-toom53.json t-toom54.json t-toom6-sqr.json t-toom62.json t-toom63.json t-toom6h.json t-toom8-sqr.json t-toom8h.json t-trunc.json t-ui_div.json t-urbui.json t-urmui.json t-urndmm.json integrated.json

rm -rf callgraphs
```
