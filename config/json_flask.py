"""
@Author: yanzx
@Date: 2022/6/9 20:02
@Description: 
"""
from flask import Flask, jsonify

from models.models import JsonResponse


class JsonFlask(Flask):
    """
    重写make_resp
    onse函数
    """

    def make_response(self, rv):
        """视图函数可以直接返回: list、dict、None"""
        if rv is None or isinstance(rv, (list, dict)):
            rv = JsonResponse.success(rv)

        if isinstance(rv, JsonResponse):
            rv = jsonify(rv.to_dict())

        return super().make_response(rv)
