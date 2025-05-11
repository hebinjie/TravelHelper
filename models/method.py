import random
from typing import Callable, List, TypeVar
from datetime import datetime
from models.user import User

T = TypeVar('T') # 泛型

# @param data: List[T]  数据列表
# @param comp: Callable[[T, T], int]  比较函数
# @return: List[T]  排序后的列表
def quick_sort(data: List[T], comp: Callable[[T, T], int], reverse: bool=False) -> List[T]:
    if len(data) <= 1:
        return data
    else:
        # 随机选择基准元素
        pivot_index = random.randint(0, len(data) - 1)
        pivot = data[pivot_index]
        left = []
        right = []
        equal = []
        for item in data:
            diff = comp(item, pivot)
            if (diff > 0 and not reverse) or (diff < 0 and reverse):
                left.append(item)
            elif (diff < 0 and not reverse) or (diff > 0 and reverse):
                right.append(item)
            else:
                equal.append(item)
        
        if len(left)>=10:
            left = quick_sort(left, comp, reverse)
            return left[:10]+left[10:] + equal + right
        elif len(left)+len(equal)>=10:
            left = quick_sort(left, comp, reverse)
            remaining = 10-len(left)
            return left + equal[:remaining] + equal[remaining:] + right
        else:
            return quick_sort(left, comp,reverse) + equal + quick_sort(right, comp, reverse)
    

def sort_data(data, sort_by, method='desc'):
    def compare(x, y):
        x_value = getattr(x, sort_by)
        y_value = getattr(y, sort_by)
        if sort_by == 'create_time':
            try:
                x_dt = datetime.fromisoformat(x_value)
                y_dt = datetime.fromisoformat(y_value)
                if x_dt > y_dt:
                    return 1 if method.lower() == 'desc' else -1
                elif x_dt < y_dt:
                    return -1 if method.lower() == 'desc' else 1
                return 0
            except ValueError:
                # 如果无法转换为日期时间，按字符串比较
                if x_value > y_value:
                    return 1 if method.lower() == 'asc' else -1
                elif x_value < y_value:
                    return -1 if method.lower() == 'asc' else 1
                return 0
        elif isinstance(x_value, (int, float)) and isinstance(y_value, (int, float)):
            if method.lower() == 'desc':
                return x_value - y_value
            return y_value - x_value
        else:
            if x_value > y_value:
                return 1 if method.lower() == 'asc' else -1
            elif x_value < y_value:
                return -1 if method.lower() == 'asc' else 1
            return 0

    return quick_sort(data, compare)

def recommend_data(data, reader_id):
    # 读取所有用户数据
    users = User.read_users()
    # 查找当前读者
    reader = next((u for u in users if u.uid == reader_id), None)
    if not reader:
        # 如果未找到读者，直接返回原数据
        return data
    # 获取读者的偏好标签
    reader_tags = reader.tags

    def compare(x, y):
        # 计算 x 日记的推荐得分
        x_match_count = len(set(x.tags).intersection(set(reader_tags)))
        x_score = (x.heat + x.rate) * 3 * x_match_count
        # 计算 y 日记的推荐得分
        y_match_count = len(set(y.tags).intersection(set(reader_tags)))
        y_score = (y.heat + y.rate) * 3 * y_match_count
        # 降序排序
        return y_score - x_score

    return quick_sort(data, compare)