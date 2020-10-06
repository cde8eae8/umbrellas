import requests
import zipfile
import json
import tempfile
import shutil
import os
import os.path
from tendo import singleton

# TODO download exceptions - no internet
# TODO global lock for other updaters
# TODO relative path -> path to script
# TODO update if app doesn't exists || new_verison > version
# TODO don't update if version is == new_version
# TODO add dependencies

def download_file(url, local_filename):
    #local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def update():
    try:
        with open(os.path.join('app', 'config.json'), 'r') as config_f:
            config = json.load(config_f)
        current_version = int(config["version"]["v"])
    except:
        current_version = 0
    repo_arch_url = 'https://github.com/cde8eae8/umbrellas/archive/master.zip'
    config_url = 'https://raw.githubusercontent.com/cde8eae8/umbrellas/master/config.json'

    print(f'requesting {config_url}...')
    r = requests.get(config_url)
    external_config = json.loads(r.text)
    newest_version = int(external_config["version"]["v"])
    print(f'Current version {current_version}')
    print(f'Newest version  {newest_version}')
    if newest_version >= current_version:
        print('updating...')
        tmpdir = tempfile.mkdtemp(prefix='sheets-gui-')
        filename = os.path.join(tmpdir, 'source.zip')
        print(f'downloading from {repo_arch_url}...', end='')
        download_file(repo_arch_url, filename)
        print(f' -- done')
        with zipfile.ZipFile(filename, "r") as zip_f:
            extractdir = os.path.join(tmpdir, 'extracted')
            print(f'extracting to {extractdir}...', end='')
            zip_f.extractall(extractdir)
            print(f' -- done')
            shutil.rmtree('./app', ignore_errors=True)
            shutil.move(os.path.join(extractdir, 'umbrellas-master'), './app')
            print('done')

if __name__ == "__main__":
    me = singleton.SingleInstance()
    update()
