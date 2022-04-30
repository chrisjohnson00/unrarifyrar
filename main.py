import requests
import unrar
import glob
import os


def main():
    sonarr_host = get_config('SONAR_HOST')
    sonarr_apikey = get_config('SONAR_APIKEY')
    response = get_request(f'{sonarr_host}/api/queue?apikey={sonarr_apikey}')
    response_json = response.json()
    for item in response_json:
        status_messages = item['statusMessages']
        for status in status_messages:
            for message in status['messages']:
                if "No files found are eligible for import" in message:
                    path = f"/data/torrents/{item['title']}/*.rar"
                    print(glob.glob(path, recursive=True))


def unrar(path):
    rar = unrar.rrarfile.RarFile(path)
    rar.extractall()


def get_request(url):
    r = requests.get(url=url)
    return r


def get_config(key):
    if os.environ.get(key):
        return os.environ.get(key)


if __name__ == '__main__':
    main()
