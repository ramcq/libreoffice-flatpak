#!/bin/sh

set -ex

branch=libreoffice-5.4.1.2

wget -O download.lst "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=download.lst;hb=${branch}"
wget -O LibreOfficeFlatpak.conf "https://gerrit.libreoffice.org/gitweb?p=core.git;a=blob_plain;f=distro-configs/LibreOfficeFlatpak.conf;hb=${branch}"

./generate_source.py

