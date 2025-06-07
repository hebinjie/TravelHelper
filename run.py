from models import create_app
from routes.diary import Diarybp
from routes.user import Userbp
from routes.spot import Spotbp
from routes.image import Imagebp

from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件中的环境变量
os.environ['PYTHONUTF8'] = '1'  # 设置环境变量，确保 Python 使用 UTF-8 编码

port = int(os.getenv('PORT', 8001))  # 从环境变量中获取端口号，默认为 8000

# 创建 Flask 应用实例
app = create_app()
# 注册蓝图，将路由与应用关联起来
app.register_blueprint(Diarybp)
app.register_blueprint(Userbp)
app.register_blueprint(Spotbp)
app.register_blueprint(Imagebp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)