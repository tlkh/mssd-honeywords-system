# Simple HoneyWords System

MSSD Assignment - Simple HoneyWords System

## Setup

1. You need python3
2. Install `flask` and `requests` (`pip3 install -r requirements.txt`)

## Running

**Terminal 1**

```shell
# delete database files and run web app
bash pre_run.sh && python3 web_server.py
```

**Terminal 2**

```shell
# run honeywords checker server
python3 honeywords_server.py
```
