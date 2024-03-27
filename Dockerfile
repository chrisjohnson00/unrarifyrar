FROM ubuntu:23.10

WORKDIR /usr/src/app

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y unrar python3 pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

CMD [ "python3", "./main.py" ]
