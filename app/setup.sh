#!/bin/bash

mkdir -p /usr/share/eviction
groupadd eviction
useradd -g eviction -d /usr/share/eviction -s $(which nologin) eviction
curl -sSL https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar -xvz > /usr/share/eviction/geckodriver
chown eviction:eviction /usr/share/eviction
chmod 700 /usr/share/eviction
sqlite3 /usr/share/eviction/cases.db "$(cat sql/*)"
chown eviction:eviction /usr/share/eviction/cases.db
python3 -m venv venv . \
  && source venv/bin/activate \
  && pip install -r requirements.txt \
  && deactivate
cp app/services/* /etc/systemd/system/
