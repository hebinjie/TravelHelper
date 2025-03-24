import os
from flask import Blueprint, request, jsonify
from models.user import User
from datetime import datetime, timedelta
from functools import wraps
import jwt

# 从环境变量中获取 SECRET_KEY，若无则使用默认值
SECRET_KEY = os.getenv('SECRET_KEY', 'travelhelper')

# 创建蓝图对象，用于组织路由
Userbp = Blueprint('user', __name__)