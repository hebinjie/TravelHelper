from pydantic import BaseModel
from typing import List, Optional
import json
# 从配置文件中导入景点文件路径配置
from config import  SPOT_FILE

# 定义景点数据模型类
class Spot(BaseModel):
    id: int                             # 景点的唯一编号
    name: str                          # 景点的名称
    description: str                   # 景点的描述
    image_url: Optional[str] = []   # 景点包含的图片链接，默认为空列表
    heat: Optional[int] = 0             # 景点的热度，默认为0
    rate: Optional[float] = 0             # 景点的评分，默认为0
    rate_num: Optional[int] = 0         # 景点的评分人数，默认为0

    # 类方法：从 JSON 文件中读取景点数据并转换为 Spot 对象列表
    @classmethod
    def read_spots(cls):
        try:
            # 打开景点 JSON 文件进行读取
            with open(SPOT_FILE, 'r') as f:
                # 读取 JSON 文件内容
                spots_data = json.load(f)
                # 将读取到的每个景点字典转换为 Spot 对象，并返回列表
                return [cls(**spot) for spot in spots_data]
        # 如果文件不存在，返回空列表
        except FileNotFoundError:
            return []

    # 类方法：将 Spot 对象列表转换为字典并写入 JSON 文件
    @classmethod
    def write_spots(cls, spots: List['Spot']):
        # 将每个 Spot 对象转换为字典
        spots_data = [spot.model_dump(exclude_unset=True) for spot in spots]
        # 打开景点 JSON 文件进行写入
        with open(SPOT_FILE, 'w') as f:
            json.dump(spots_data, f, indent=4)