from pydantic import BaseModel
from typing import List, Optional
import json
# 从配置文件中导入日记文件路径配置
from config import DIARY_FILE, COMPRESSED_DIARY_FILE
from models.huffman import compress, decompress

# 定义日记数据模型类
class Diary(BaseModel):
    id: int                             # 日记的唯一编号
    uid: Optional[int] = 0              # 日记的作者编号
    username: Optional[str] = None      # 日记的作者用户名
    title: str                          # 日记的标题
    content: str                        # 日记的内容  
    images: Optional[List[str]] = []    # 日记包含的图片路径列表，默认为空列表
    heat: Optional[int] = 0             # 日记的热度，默认为0
    create_time: Optional[str]          # 日记的创建时间
    update_time: Optional[str]          # 日记的更新时间
    rate: Optional[float] = 0           # 日记的评分，默认为0
    rate_num: Optional[int] = 0         # 日记的评分人数，默认为0
    tags: Optional[List[str]] = []      # 日记的标签列表
    type: Optional[str] = None          # 日记对应的美食类型

    # 类方法：从 JSON 文件中读取日记数据并转换为 Diary 对象列表
    @classmethod
    def read_diaries(cls):
        try:
            # 解压缩文件
            decompress(COMPRESSED_DIARY_FILE, DIARY_FILE)
            # 打开日记 JSON 文件进行读取
            with open(DIARY_FILE, 'r') as f:
                # 读取 JSON 文件内容
                diaries_data = json.load(f)
                # 将读取到的每个日记字典转换为 Diary 对象，并返回列表
                return [cls(**diary) for diary in diaries_data]
        # 如果文件不存在，返回空列表
        except FileNotFoundError:
            return []

    # 类方法：将 Diary 对象列表转换为字典并写入 JSON 文件
    @classmethod
    def write_diaries(cls, diaries: List['Diary']):
        # 将每个 Diary 对象转换为字典
        diaries_data = [diary.model_dump(exclude_unset=True) for diary in diaries]
        # 打开日记 JSON 文件进行写入
        with open(DIARY_FILE, 'w') as f:
            json.dump(diaries_data, f, indent=4)
        # 压缩文件
        compress(DIARY_FILE, COMPRESSED_DIARY_FILE)