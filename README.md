## PyPi Dependencies

``` 
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pygogo requests unrar
pip freeze > requirements.txt
sed -i '/pkg_resources/d' requirements.txt
```