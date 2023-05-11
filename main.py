import requests
import glob
import os
import pygogo as gogo
import subprocess
import tempfile
import shutil

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main():
    logger.info("Starting")
    sonarr_host = get_config('SONARR_HOST')
    sonarr_apikey = get_config('SONARR_APIKEY')
    check_sonarr_queue_for_unrar(sonarr_apikey, sonarr_host)
    radarr_host = get_config('RADARR_HOST')
    radarr_apikey = get_config('RADARR_APIKEY')
    check_radarr_queue_for_unrar(radarr_apikey, radarr_host)
    logger.info("Done")


def check_sonarr_queue_for_unrar(apikey, host):
    logger.info(f'Checking {host}')
    response = get_request(f'{host}/api/queue?apikey={apikey}')
    response_json = response.json()
    logger.debug(response_json)
    for item in response_json:
        status_messages = item['statusMessages']
        for status in status_messages:
            for message in status['messages']:
                if "No files found are eligible for import" in message:
                    unrar_files(item)
            if "One or more episodes expected in this release were not imported or missing" in status['title']:
                unrar_files(item)


def check_radarr_queue_for_unrar(apikey, host):
    logger.info(f'Checking {host}')
    response = get_request(f'{host}/api/v3/queue', {'X-Api-Key': apikey})
    response_json = response.json()
    for item in response_json['records']:
        status_messages = item['statusMessages']
        for status in status_messages:
            for message in status['messages']:
                if "No files found are eligible for import" in message or "Sample" in message:
                    unrar_files(item)
            if ("One or more episodes expected in this release were not imported or missing" in status['title']
                    or "Found archive file" in status['title']):
                unrar_files(item)


def unrar_files(item):
    torrent_path = '/torrents/'
    extract_path = f"{torrent_path}{item['title']}/"
    temp_dir = tempfile.mkdtemp()
    glob_search = f"{extract_path}*.rar"
    rar_files = glob.glob(glob_search, recursive=True)
    for path in rar_files:
        logger.info(f'Unraring {path}')
        command = ['unrar', 'e', path, temp_dir]
        logger.info(f'Unrar {path} to {temp_dir}')
        subprocess.run(command, check=True)
        move_from_temp_dir(temp_dir, extract_path)


def move_from_temp_dir(source_dir, dest_dir):
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path):
            logger.info(f'Moving {file_path} to {dest_dir}')
            shutil.move(file_path, dest_dir)


def get_request(url, headers={}):
    r = requests.get(url=url, headers=headers)
    return r


def get_config(key):
    if os.environ.get(key):
        return os.environ.get(key)


if __name__ == '__main__':
    main()
