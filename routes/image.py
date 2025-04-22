from flask import Blueprint, request, jsonify
import os
import base64
from routes.user import token_required
from config import IMAGE_FOLDER

# 创建蓝图对象
Imagebp = Blueprint('image', __name__)

@Imagebp.route('/api/img', methods=['POST'])
@token_required
def upload_image():

    # 检查请求是否包含文件部分
    if 'data' not in request.files:
        return jsonify({'code': -1, 'message': 'No file part'}), 400
    file = request.files['data']
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'code': -1, 'message': 'No selected file'}), 400
    
    # 处理文件名（如果前端已用url safe base64编码，这里解码获取原始文件名，不过前端说不用管，暂按原样处理）
    # name = request.form.get('name')
    # if name:
    #     try:
    #         decoded_name = base64.urlsafe_b64decode(name).decode('utf-8')
    #         file.filename = decoded_name
    #     except Exception as e:
    #         return jsonify({'code': -1, 'message': f'Error decoding name: {str(e)}'}), 400

    # 保存文件
    file_path = os.path.join(IMAGE_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'code': 200, 'message': 'Image uploaded successfully'}), 200