from pydantic import BaseModel
from typing import List, Optional
import json
import os
import tempfile
# 从配置文件中导入日记文件路径配置
from config import COMPRESSED_DIARY_FILE
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

    # 类方法：从压缩文件中读取日记数据并转换为 Diary 对象列表
    @classmethod
    def read_diaries(cls):
        try:
        # 创建唯一临时文件
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
                temp_file = tmp.name
            # 解压缩到唯一临时文件
            decompress(COMPRESSED_DIARY_FILE, temp_file)
        
            with open(temp_file, 'r') as f:
                diaries_data = json.load(f)
                diaries = [cls(**diary) for diary in diaries_data]
            os.remove(temp_file)
            return diaries
        except FileNotFoundError:
            return []

    # 类方法：将 Diary 对象列表转换为字典并写入压缩文件
    @classmethod
    def write_diaries(cls, diaries: List['Diary']):
        # 将每个 Diary 对象转换为字典
        diaries_data = [diary.model_dump(exclude_unset=True) for diary in diaries]
        # 创建唯一临时文件
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            temp_file = tmp.name
        with open(temp_file, 'w') as f:
            json.dump(diaries_data, f, indent=4)
        compress(temp_file, COMPRESSED_DIARY_FILE)
        os.remove(temp_file)