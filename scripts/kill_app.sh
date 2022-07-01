
ps ux | grep -E 'app.py' | grep -v grep |awk '{print $2}' |xargs kill -s 9
