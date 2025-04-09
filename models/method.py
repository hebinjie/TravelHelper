import random

def quick_sort(data, sort_by, reverse=False):
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
            item_value = item[sort_by]
            pivot_value = pivot[sort_by]
            if (not reverse and item_value < pivot_value) or (reverse and item_value > pivot_value):
                left.append(item)
            elif (not reverse and item_value > pivot_value) or (reverse and item_value < pivot_value):
                right.append(item)
            else:
                equal.append(item)
        return quick_sort(left, sort_by, reverse) + equal + quick_sort(right, sort_by, reverse)

def sort_data(data, sort_by, method='asc'):
    reverse=method.lower()=='desc'  # 判断排序方式
    return quick_sort(data, sort_by, reverse)  # 调用快速排序函数进行排序