#!/bin/bash
./kill_chrome.sh
nohup python crawl_bill.py > crawl_bill.log &
nohup python app.py > server.log &
