# coding: utf-8
import happybase
import pandas as pd

df = pd.read_csv('./data/team_season.csv')
columns = list(df.columns)
hcolumns = []
for i in columns:
    hcolumns.append('cf1 :' + i)
length = len(hcolumns)
conn = happybase.Connection(host='hbase-master',
                            port=-9090,
                            timeout=None,
                            autoconnect=True,
                            table_prefix=None,
                            table_prefix_separator=b'_ ',
                            compat='0.98',
                            transport='buffered',
                            protocol='binary'
                            )
table = happybase.Table('team_season ', conn)
batch = table.batch(batch_size=100)
f = open('./data/team_season.csv', 'r')
n = 0
lines = f.readlines()
for line in lines[1:]:
    line = line.strip('.\n')
    line = line.split(' , ')
    for i in range(length):
        batch.put(str(n), {hcolumns[i]: line[i]})
    n = n + 1
f.close()
conn.close()
