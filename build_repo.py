# Baut docs/repo (Kodi-Repository) neu. Aufruf: python3 build_repo.py
import hashlib, os, re, zipfile

B = 'https://maikpeters1511.github.io/xtream/repo/'
R = 'docs/repo'
PLUGIN = 'plugin.video.xstream'
EXCLUDE_DIRS = {'.git', 'docs', '__pycache__'}
EXCLUDE_FILES = {'.DS_Store', 'youtube_keys.json', '.gitignore', 'build_repo.py'}


def strip(s):
    return re.sub(r'<\?xml[^>]*\?>\s*', '', s).strip()


ver = re.search(r'<addon[^>]*version="([^"]+)"', open('addon.xml', encoding='utf-8').read()).group(1)
repo_xml = open('docs/repository.xstream.addon.xml', encoding='utf-8').read().replace('{B}', B)

repo_ver = re.search(r'<addon[^>]*version="([^"]+)"', repo_xml).group(1)
REPO = 'repository.xstream'
os.makedirs(R + '/' + REPO, exist_ok=True)
for f in os.listdir(R + '/' + REPO):
    os.remove(os.path.join(R, REPO, f))
for f in os.listdir('docs'):
    if f.startswith(REPO + '-') and f.endswith('.zip'):
        os.remove(os.path.join('docs', f))
for target in (f'{R}/{REPO}/{REPO}-{repo_ver}.zip', f'docs/{REPO}-{repo_ver}.zip'):
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(REPO + '/addon.xml', repo_xml)
# index.html verweist auf die aktuelle Repository-ZIP
idx = open('docs/index.html', encoding='utf-8').read()
idx = re.sub(r'repository\.xstream-[\d.]+\.zip', f'{REPO}-{repo_ver}.zip', idx)
open('docs/index.html', 'w', encoding='utf-8').write(idx)

os.makedirs(R + '/' + PLUGIN, exist_ok=True)
for f in os.listdir(R + '/' + PLUGIN):
    os.remove(os.path.join(R, PLUGIN, f))

with zipfile.ZipFile(f'{R}/{PLUGIN}/{PLUGIN}-{ver}.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for d, ds, fs in os.walk('.'):
        ds[:] = [x for x in ds if x not in EXCLUDE_DIRS]
        for f in fs:
            if f in EXCLUDE_FILES or f.endswith('.zip'):
                continue
            p = os.path.join(d, f)
            zf.write(p, PLUGIN + '/' + os.path.relpath(p, '.'))

xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'
       + strip(open('addon.xml', encoding='utf-8').read()) + '\n' + strip(repo_xml) + '\n</addons>\n')
open(R + '/addons.xml', 'w', encoding='utf-8').write(xml)
open(R + '/addons.xml.md5', 'w').write(hashlib.md5(xml.encode()).hexdigest())
print('gebaut:', ver)
