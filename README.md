## PyPi Dependencies

``` 
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pygogo requests
pip freeze > requirements.txt
sed -i '/pkg_resources/d' requirements.txt
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