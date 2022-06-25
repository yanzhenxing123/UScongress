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
# 线程池
pool = ThreadPoolExecutor(max_workers=3)

# 解决路径问题
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# cur_path = os.path.abspath(os.path.dirname(__file__))
# root_path = os.path.split(cur_path)[0]
# sys.path.append(root_path)


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
    data['crawl_nums'] = int(data['crawl_nums'])
    utils.print_dict(data)
    # 异步爬取数据
    spider.pool.submit(spider.main, data)
    return JsonResponse.success()


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5000, debug=False)
