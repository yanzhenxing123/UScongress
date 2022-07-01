ps ux | grep -E 'app.py' | grep -v grep |awk '{print $2}' |xargs kill -s 9
ps ux | grep -E 'crawl_bill.py' | grep -v grep |awk '{print $2}' |xargs kill -s 9
ps ux | grep -E 'chrome' | grep -v grep |awk '{print $2}' |xargs kill -s 9