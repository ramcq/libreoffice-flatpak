#!/usr/bin/python

import json, os, re, sys

distro_conf = 'LibreOfficeFlatpak.conf'
download_lst = 'download.lst'
json_in = 'flatpak-manifest.in'
json_out = 'org.libreoffice.LibreOffice.json'
base_url = 'https://dev-www.libreoffice.org/src'
dest_path = 'external/tarballs'

branch = sys.argv[1]
if len(sys.argv) > 2:
    commit = sys.argv[2]
else:
    commit = None

external_projects = ['collada2gltf', 'pdfium', 'opencollada', 'ucpp', 'xmlsec']
external_projects += ['font_caladea', 'font_carlito', 'font_dejavu',
                      'font_gentium', 'font_liberation_narrow',
                      'font_liberation', 'font_linlibertineg', 'font_opensans',
                      'font_ptserif', 'font_sourcecode', 'font_sourcesans',
                      'font_emojione_color']
with open(distro_conf, 'r') as dc:
    for line in dc:
        line = line.rstrip()
        if line.startswith("--without-system-"):
            project = line[17:]
            # skip external headers
            if project in ['bluez', 'odbc', 'sane']:
                continue
            if project == 'gpgmepp':
                external_projects += ['gpgme', 'assuan', 'gpgerror']
                continue
            if project == 'liblangtag':
                external_projects += ['langtagreg']
            if project == 'redland':
                external_projects += ['raptor', 'rasqal']
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

# keep the two static defined modules, update the branch we want to fetch,
# then replace all of the generated modules with the newly-generated ones
j['modules'][0]['sources'] = j['modules'][0]['sources'][0:2]
j['modules'][0]['sources'][0]['branch'] = branch
if commit:
    j['modules'][0]['sources'][0]['branch'] = commit
j['modules'][0]['sources'] += sources

with open(json_out, 'w') as jo:
    json.dump(j, jo, indent=4)
