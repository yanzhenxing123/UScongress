import os
import sys
import spider
import utils
from flask import request
from flask_cors import CORS
from config.json_flask import JsonFlask
from concurrent.futures import ThreadPoolExecutor
from models.models import JsonResponse

app = JsonFlask(__name__)

# 解决路径问题
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

# 线程池
pool = ThreadPoolExecutor(max_workers=3)
# 跨域问题
CORS(app, supports_credentials=True, resources=r'/*')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/crawl', methods=['POST'])
def crawl():
    form = request.form
    data = {}
    for key in form:
        data[key] = form.getlist(key) if '[]' in key else form.get(key)
    # 异步爬取数据
    pool.submit(spider.main, data)
    return JsonResponse.success()


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5000, debug=False)
