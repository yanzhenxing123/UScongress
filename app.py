import os
import sys
import spider
import utils
from flask import request
from flask_cors import CORS
from config.json_flask import JsonFlask
from models.models import JsonResponse

app = JsonFlask(__name__)

# 解决路径问题
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
CORS(app, resources=r'/*')

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
    utils.pool.submit(spider.main, data)
    return JsonResponse.success()


if __name__ == '__main__':
    # 跨域问题
    app.run(host="0.0.0.0", threaded=True, port=5000, debug=False)
