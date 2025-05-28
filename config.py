import os
import json
from models.huffman import compress

# 日记存储的 JSON 文件(若无JSON文件则创建一个)
DIARY_FILE = 'diaries.json'
if not os.path.exists(DIARY_FILE):
    empty_diary = json.dumps([])
    compressed_diary = compress(empty_diary)
    with open(DIARY_FILE, 'w') as f:
        f.write(compressed_diary)

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