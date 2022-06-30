#!/bin/bash
./kill_chrome.sh
nohup python crawl_bill.py > logs/crawl_bill.log &
nohup python app.py > logs/server.log &
