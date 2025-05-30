import os
import json

# 压缩后的日记文件
COMPRESSED_DIARY_FILE = 'diaries_compressed.bin'

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

# 图片存储的目录(若无目录则创建一个)
IMAGE_FOLDER = 'images'
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)