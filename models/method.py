import random
from typing import Callable, List, TypeVar

T = TypeVar('T') # 泛型

# @param data: List[T]  数据列表
# @param comp: Callable[[T, T], int]  比较函数
# @return: List[T]  排序后的列表
def quick_sort(data: List[T], comp: Callable[[T, T], int]) -> List[T]:
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
            if comp(item, pivot) > 0:
                left.append(item)
            elif comp(item, pivot) < 0:
                right.append(item)
            else:
                equal.append(item)
        return quick_sort(left, comp) + equal + quick_sort(right, comp)

def sort_data(data, sort_by, method='desc'):
    if method.lower()=='desc':# 判断排序方式
        comp = lambda x, y: getattr(x, sort_by) - getattr(y, sort_by)
    else:
        comp = lambda x, y: getattr(y, sort_by) - getattr(x, sort_by)
    return quick_sort(data, comp)  # 调用快速排序函数进行排序