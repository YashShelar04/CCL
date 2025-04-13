#!/bin/bash
apt update
apt install -y python3-pip
pip3 install flask mysql-connector-python
git clone https://github.com/your-username/sql-injection-prevention-app.git
cd sql-injection-prevention-app/backend
nohup python3 app.py &
