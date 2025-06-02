import os
import json
import time
import random
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 用户映射关系
USER_MAP = {
    1: "123456",
    2: "123",
    3: "瞿志国",
    4: "历俊杰",
    5: "linnuofan"
}

# 标签库（确保标签重复性）
TAGS_POOL = ["自然", "历史", "美食", "旅行", "摄影", "文化", "城市", "休闲"]

# 美食类型库
FOOD_TYPES = ["北京菜", "川菜", "法餐", "粤菜", "日料", "东南亚菜", "甜品"]

# 生成时间范围
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

def generate_random_time():
    """生成随机时间"""
    delta = END_DATE - START_DATE
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 24*60*60)
    base_time = START_DATE + timedelta(days=random_days)
    random_time = base_time + timedelta(seconds=random_seconds)
    return random_time.strftime("%Y-%m-%d %H:%M:%S")

def validate_diary(diary):
    """验证日记格式"""
    try:
        # 必填字段检查
        required_fields = ['id', 'uid', 'username', 'title', 'content', 'tags', 'type']
        if not all(field in diary for field in required_fields):
            return False
            
        # 内容长度检查
        if len(diary['content']) < 30:
            return False
            
        # 用户映射验证
        if diary['uid'] not in USER_MAP or diary['username'] != USER_MAP[diary['uid']]:
            return False
            
        # 数值范围检查
        if not (0 <= diary.get('rate', 5) <= 5 and diary.get('rate_num', 0) >= 0 and diary.get('heat', 0) >= 0):
            return False
            
        # 时间格式验证
        datetime.strptime(diary['create_time'], "%Y-%m-%d %H:%M:%S")
        datetime.strptime(diary['update_time'], "%Y-%m-%d %H:%M:%S")
        
        # 标签有效性检查
        if not all(tag in TAGS_POOL for tag in diary['tags']):
            return False
            
        return True
        
    except Exception as e:
        print(f"验证失败: {str(e)}")
        return False

def generate_prompt(batch_size):
    """生成提示词模板"""
    return f"""
你是一个日记生成助手，请生成{batch_size}篇符合以下要求的日记：

1. 字段要求：
   - id（唯一编号，从1开始递增）
   - uid（用户ID，必须来自 {list(USER_MAP.keys())}）
   - username（必须与uid对应，映射关系：{USER_MAP}）
   - title（吸引人的标题）
   - content（至少30字，描述具体场景）
   - images（可选图片路径数组）
   - heat（热度值，≥0整数）
   - create_time（创建时间）
   - update_time（更新时间）
   - rate（评分，0-5）
   - rate_num（评分人数，≥0整数）
   - tags（从 {TAGS_POOL} 中选择）
   - type（美食类型，从 {FOOD_TYPES} 选择）

2. 生成规则：
   - 时间格式必须为 YYYY-MM-DD HH:MM:SS
   - 标签必须来自指定标签库
   - 确保内容多样性（涵盖不同主题）
   - 返回严格的JSON数组格式
   - 不要包含任何额外信息
"""

def generate_diaries(total=50, batch_size=5, max_retries=3):
    """批量生成日记"""
    all_diaries = []
    current_id = 1
    
    while len(all_diaries) < total:
        remaining = total - len(all_diaries)
        current_batch_size = min(batch_size, remaining)
        
        for attempt in range(max_retries):
            try:
                completion = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是一个日记生成助手，严格遵循格式要求和业务规则"},
                        {"role": "user", "content": generate_prompt(current_batch_size)}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7
                )
                
                response = json.loads(completion.choices[0].message.content)
                
                # 处理生成结果
                for diary in response:
                    # 强制覆盖ID确保唯一性
                    diary['id'] = current_id
                    current_id += 1
                    
                    # 强制生成时间
                    diary['create_time'] = generate_random_time()
                    diary['update_time'] = generate_random_time()
                    
                    # 验证并添加有效日记
                    if validate_diary(diary):
                        all_diaries.append(diary)
                
                print(f"成功生成 {len(all_diaries)}/{total} 篇日记")
                break
                
            except Exception as e:
                print(f"生成失败（尝试 {attempt+1}/{max_retries}）: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        
        time.sleep(2)  # 防止API限流
    
    return all_diaries[:total]  # 确保数量准确

if __name__ == "__main__":
    print("🚀 开始生成日记数据...")
    diaries = generate_diaries()
    
    # 保存结果
    output_path = "generated_diaries.json"
    with open(output_path, "w") as f:
        json.dump(diaries, f, indent=4)
    
    print(f"\n✅ 日记生成完成！共生成 {len(diaries)} 篇日记")
    print(f"📁 文件已保存至: {os.path.abspath(output_path)}")
