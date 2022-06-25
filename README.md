# UScongress

后台：Flask Server

爬虫：undetected_chrome + selenium

数据库：Mysql + Redis



## 前端

爬虫控制界面，与[Advance Search](https://www.congress.gov/advanced-search/legislation)一致 

![image-20220625142648026](http://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/typora/202206/25/142648-327446.png)



## 运行过程

由于有cloudflare盾，所以用undetected chrome，根据爬虫控制界面拼接URL，然后请求，获取主页面信息，入库，将要请求的bill_url存到redis，开启新线程从redis中拿数据，重新请求，再入库，保证每一条信息的完整性。



## 使用

下载依赖

`pip install -r req.txt`

下载对应版本的chromedriver，在代码utils.py中修改chromedriver文件路径

执行`python app.py` 启动flask server，即开启了5000端口

运行前端 index.html文件，勾选参数，确认即可爬虫启动。