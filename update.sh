#!/bin/sh

set -ex

branch=libreoffice-5.4.1.1

wget -O download.lst "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=download.lst;hb=${branch}"
wget -O LibreOfficeFlatpak.conf "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=distro-configs/LibreOfficeFlatpak.conf;hb=${branch}"

xmlsec_flag="--without-system-xmlsec"
if ! grep -q -- "${xmlsec_flag}" LibreOfficeFlatpak.conf; then
  echo "${xmlsec_flag}" >>LibreOfficeFlatpak.conf
fi

./generate_source.py

