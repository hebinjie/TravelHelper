from pydantic import BaseModel
from typing import List, Optional
import json
# 从配置文件中导入用户文件路径配置
from config import USER_FILE

class User(BaseModel):
    uid: int
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    diary_count: Optional[int] = 0
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0
    tags: Optional[List[str]] = []     # 用户偏好的标签列表

 # 类方法：从 JSON 文件中读取用户数据并转换为 User 对象列表
    @classmethod
    def read_users(cls):
        try:
            # 打开用户 JSON 文件进行读取
            with open(USER_FILE, 'r') as f:
                # 读取 JSON 文件内容
                users_data = json.load(f)
                # 将读取到的每个用户字典转换为 User 对象，并返回列表
                return [cls(**user) for user in users_data]
        # 如果文件不存在，返回空列表
        except FileNotFoundError:
            return []

    # 类方法：将 User 对象列表转换为字典并写入 JSON 文件
    @classmethod
    def write_users(cls, users: List['User']):
        # 将每个 User 对象转换为字典
        users_data = [user.model_dump(exclude_unset=True) for user in users]
        # 打开用户 JSON 文件进行写入
        with open(USER_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
    
    # 类方法：根据用户id查找用户名
    @classmethod
    def get_username_by_uid(cls, uid: int) -> Optional[str]:
        users = cls.read_users()
        user = next((user for user in users if user.uid == uid), None)
        return user.username if user else None