from models import create_app
from routes.diary import Diarybp

# 创建 Flask 应用实例
app = create_app()
# 注册蓝图，将路由与应用关联起来
app.register_blueprint(Diarybp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)