
ps ux | grep -E 'chrome' | grep -v grep |awk '{print $2}' |xargs kill -s 9
