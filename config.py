import os
import json

# 日记存储的 JSON 文件(若无JSON文件则创建一个)
DIARY_FILE = 'diaries.json'
if not os.path.exists(DIARY_FILE):
    with open(DIARY_FILE, 'w') as f:
        json.dump([], f)

# 用户存储的 JSON 文件(若无JSON文件则创建一个)
USER_FILE = 'users.json'
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump([], f)

# 景点存储的 JSON 文件(若无JSON文件则创建一个)
SPOT_FILE = 'spots.json'
if not os.path.exists(SPOT_FILE):
    with open(SPOT_FILE, 'w') as f:
        json.dump([], f)