#!/usr/bin/python

import json, os, re

distro_conf = 'LibreOfficeFlatpak.conf'
download_lst = 'download.lst'
base_url = 'https://dev-www.libreoffice.org/src'
dest_path = 'external/tarballs'
json_out = 'org.libreoffice.LibreOffice.json'
json_in = json_out + '.in'

external_projects = []
with open(distro_conf, 'r') as dc:
    for line in dc:
        line = line.rstrip()
        if line.startswith("--without-system-"):
            project = line[17:]
            # skip external headers
            if project in ['bluez', 'odbc', 'sane']:
                continue
            external_projects += [project]

download_vars = {}
with open(download_lst, 'r') as dl:
    for line in dl:
        m = re.match('^export\s+(\S+)\s*:=\s*(\S+)$', line)

        if not m:
            continue

        key = m.group(1)
        val = m.group(2)

        m = re.match(r'(.*)\$\((\S+)\)(.*)', val)
        if m:
            val = m.group(1) + download_vars[m.group(2)] + m.group(3)

        download_vars[key] = val

sources = []
for project in external_projects:
    try_keys = [project]
    if project.startswith('lib'):
        try_keys += [project[3:]]
    else:
        try_keys += ['lib' + project]
    if project.endswith('pp'):
        try_keys += [project[:-2]]

    for key in try_keys:
        tarball_key = key.upper() + '_TARBALL'
        shasum_key = key.upper() + '_SHA256SUM'
        if download_vars.has_key(tarball_key):
            break

    if project in ['libgltf']:
        url = os.path.join(base_url, project, download_vars[tarball_key])
    else:
        url = os.path.join(base_url, download_vars[tarball_key])
    dest_filename = os.path.join(dest_path, download_vars[tarball_key])

    sources += [{
            'type': 'file',
            'url': url,
            'sha256': download_vars[shasum_key],
            'dest-filename': dest_filename
        }]

with open(json_in, 'r') as ji:
    j = json.load(ji)

j['modules'][0]['sources'] += sources

with open(json_out, 'w') as jo:
    json.dump(j, jo, indent=4)
