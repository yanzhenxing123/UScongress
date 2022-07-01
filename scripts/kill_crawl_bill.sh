
ps ux | grep -E 'crawl_bill.py' | grep -v grep |awk '{print $2}' |xargs kill -s 9
