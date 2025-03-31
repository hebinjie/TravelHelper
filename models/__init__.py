from flask import Flask
from flask_cors import CORS
# 从配置文件中导入日记文件路径配置
from config import DIARY_FILE
from config import USER_FILE

def create_app():
    # 创建 Flask 应用实例
    app = Flask(__name__)
    # 将文件路径配置添加到 Flask 应用的配置中
    app.config['DIARY_FILE'] = DIARY_FILE
    app.config['USER_FILE'] = USER_FILE
    # 配置跨域资源共享（CORS）
    CORS(app, supports_credentials=True)  # 支持跨域请求，允许携带凭证（如 Cookies）
    # 返回创建并配置好的 Flask 应用实例
    return app