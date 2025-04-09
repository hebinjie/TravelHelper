from models import create_app
from routes.diary import Diarybp
from routes.user import Userbp
from routes.spot import Spotbp

# 创建 Flask 应用实例
app = create_app()
# 注册蓝图，将路由与应用关联起来
app.register_blueprint(Diarybp)
app.register_blueprint(Userbp)
app.register_blueprint(Spotbp)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)