# -*- coding: utf-8 -*-
from flask import render_template

from . import main


# 全局错误：app_errorhandler，蓝本局部错误：errorhandler
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403
