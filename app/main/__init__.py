# -*- coding: utf-8 -*-
"""Flask 使用蓝本可以避免@app.route()修饰器中app仍未定义的困境。
    蓝本和程序类似，也可以定义路由。不同的是，在蓝本中定义的路由处于休眠状态，
    直到蓝本注册到程序上后，路由才真正成为程序的一部分。
    使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。
"""

from flask import Blueprint

from ..models.permission_model import Permission

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


from . import views, errors
