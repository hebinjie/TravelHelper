from flask import Blueprint, request, jsonify
from models.user import User
from datetime import datetime, timedelta,timezone
from functools import wraps
import jwt

# 从环境变量中获取 SECRET_KEY，若无则使用默认值
SECRET_KEY = 'travelhelper'

# 创建蓝图对象，用于组织路由
Userbp = Blueprint('user', __name__)

# 生成 JWT 令牌的函数
def generate_token(user):
    # 定义 JWT 令牌的负载，包含用户 ID 和过期时间
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    # 生成 JWT 令牌
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# 验证 JWT 令牌的装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 获取 Authorization 字段
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # 去除令牌前缀 'Bearer '
            token = token.replace('Bearer ', '')
            # 对令牌进行解码
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # 获取用户 ID
            user_id = data.get('user_id')
            # 读取所有用户数据
            users = User.read_users()
            # 查找与用户 ID 匹配的用户
            user = next((u for u in users if u.id == user_id), None)
            if not user:
                return jsonify({'message': 'Invalid token!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(*args, **kwargs)
    
    return decorated

# 用户注册接口
@Userbp.route('/api/register', methods=['POST'])
def register():
    try:
        # 获取请求中的 JSON 数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required!'}), 400

        # 读取所有用户数据
        users = User.read_users()
        # 检查是否存在同名用户
        if next((u for u in users if u.username == username), None):
            return jsonify({'message': 'Username already exists!'}), 400

        # 创建新的 User 对象
        new_user = User(id=len(users) + 1, username=username, password=password, avatar=None, bio=None, diary_count=0, followers_count=0, following_count=0)
        # 将新用户添加到用户列表中
        users.append(new_user)
        User.write_users(users)

        # 返回注册成功信息和生成的令牌，状态码为 201
        return jsonify({'code': '200','message': 'User registered successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 用户登录接口
@Userbp.route('/api/login', methods=['POST'])
def login():
    try:
        # 获取请求中的 JSON 数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required!'}), 400

        # 读取所有用户数据
        users = User.read_users()
        # 查找匹配的用户对象
        user = next((u for u in users if u.username == username), None)

        if not user or user.password != password:
            return jsonify({'message': 'Invalid username or password!'}), 401

        # 为登录用户生成 JWT 令牌
        token = generate_token(user)
        
        return jsonify({'code': '200','token': token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取指定编号用户信息
@Userbp.route('/api/user/<int:id>', methods=['GET'])
def GetUserInfo(id):
    try:
        # 从 JSON 文件中读取用户数据
        users = User.read_users()
        # 查找指定编号的用户
        user= next((user for user in users if user.id == id), None)

        if user:
            return jsonify(user.model_dump(exclude={"password","id"})), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新指定编号用户信息
@Userbp.route('/api/user/<int:id>', methods=['PUT'])
def UpdateUserInfo(id):
    try:
        # 获取请求中的 JSON 数据
        data = request.get_json()
        # 从 JSON 文件中读取用户数据
        users = User.read_users()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # 查找指定 id 的用户
        index = next((i for i, u in enumerate(users) if u.id == id), None)

        if index is not None:
            user = users[index]
            avatar = data.get('avatar')
            bio = data.get('bio')

            if avatar:
                user.avatar = avatar
            if bio:
                user.bio = bio

            # 更新列表中的对应用户信息
            users[index] = user
            # 将更新后的用户列表写入 JSON 文件
            User.write_users(users)

            return jsonify({'code': '200','message': 'User updated successfully!'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500