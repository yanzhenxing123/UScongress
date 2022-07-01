#!/bin/bash
bash scripts/kill_app.sh
bash scripts/kill_chrome.sh
bash scripts/kill_crawl_bill.sh
nohup python crawl_bill.py > logs/crawl_bill.log &
nohup python app.py > logs/server.log &
