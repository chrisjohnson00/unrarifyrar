## PyPi Dependencies

``` 
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pygogo requests
pip freeze > requirements.txt

```

## Running

```commandline
docker run --rm -e SONARR_HOST=http://192.168.1.131:8989 \
    -e SONARR_APIKEY=xxxx \
    -e RADARR_HOST=http://192.168.1.131:7878 \
    -e RADARR_APIKEY=xxxx \
    -v /data/torrents/:/torrents \
    --user 1000:1000 \
    chrisjohnson00/unrarifyrar
```

```shell
export SONARR_HOST=http://192.168.1.131:8989
export SONARR_APIKEY=xxxx 
export RADARR_HOST=http://192.168.1.131:7878
export RADARR_APIKEY=xxxx
python3 main.py
```