#!/bin/sh

set -ex

#branch=libreoffice-5-4
branch=master
commit=b9ddf19ca151d2c7f7315fc26138e5b2b4d4ab8d

if [ -n "${commit}" ]; then
  refspec="${commit}"
else
  refspec="${branch}"
fi

wget -O download.lst "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=download.lst;hb=${refspec}"
wget -O LibreOfficeFlatpak.conf "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=distro-configs/LibreOfficeFlatpak.conf;hb=${refspec}"
wget -O flatpak-manifest.in "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=solenv/flatpak-manifest.in;hb=${refspec}"

./generate_source.py "${branch}" "${commit}"

