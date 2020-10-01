import requests
import zipfile

# download exceptions - no internet
# global lock for other updaters

def download_file(url, local_filename):
    #local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                print('.', end='')
                f.write(chunk)
    return local_filename

def update():
    with open('config.json', 'r') as config_f:
        config = json.load(config_f)
    url='https://github.com/cde8eae8/umbrellas/archive/master.zip'
    download_file(url, filename)
    zipfile.ZipFile(filename, "r") as zip_f:
        zip_f.extractall("binary")


if __name__ == "__main__":
    update()
