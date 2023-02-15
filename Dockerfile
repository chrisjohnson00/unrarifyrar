FROM ubuntu:22.10

WORKDIR /usr/src/app

RUN apt update && \
    apt install -y unrar python3 pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./main.py" ]
