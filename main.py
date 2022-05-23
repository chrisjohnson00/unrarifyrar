import requests
import glob
import os
import pygogo as gogo
import subprocess

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main():
    logger.info("Starting")
    sonarr_host = get_config('SONAR_HOST')
    sonarr_apikey = get_config('SONAR_APIKEY')
    response = get_request(f'{sonarr_host}/api/queue?apikey={sonarr_apikey}')
    response_json = response.json()
    for item in response_json:
        status_messages = item['statusMessages']
        for status in status_messages:
            for message in status['messages']:
                if "No files found are eligible for import" in message:
                    unrar_files(item)
            if "One or more episodes expected in this release were not imported or missing" in status['title']:
                unrar_files(item)
    logger.info("Done")


def unrar_files(item):
    torrent_path = '/torrents/'
    extract_path = f"{torrent_path}{item['title']}/"
    glob_search = f"{extract_path}*.rar"
    rar_files = glob.glob(glob_search, recursive=True)
    for path in rar_files:
        logger.info(f'Unraring {path}')
        command = ['unrar', 'e', '-o-', path, extract_path]
        subprocess.run(command, check=True)


def get_request(url):
    r = requests.get(url=url)
    return r


def get_config(key):
    if os.environ.get(key):
        return os.environ.get(key)


if __name__ == '__main__':
    main()
