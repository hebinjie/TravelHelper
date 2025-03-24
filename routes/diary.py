from flask import Blueprint, request, jsonify
from models.diary import Diary
import datetime

# 创建蓝图对象，用于组织路由
Diarybp = Blueprint('diary', __name__)

# 发布日记
@Diarybp.route('/api/diary', methods=['POST'])
def CreateDiary():
    try:
        # 获取前端传递的 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # 从 JSON 数据中获取日记标题
        title = data.get('title')
        # 从 JSON 数据中获取日记内容
        content = data.get('content')
        # 从 JSON 数据中获取图片路径列表，默认为空列表
        image_paths = data.get('images', [])

        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400

        # 从 JSON 文件中读取现有的日记数据
        diaries = Diary.read_diaries()
        # 生成新的日记编号，如果没有现有日记则为1，否则为最大编号加1
        new_id = max([diary.id for diary in diaries]) + 1 if diaries else 1

        # 获取当前时间
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        # 创建新的日记对象
        new_diary = Diary(id=new_id, title=title, content=content, images=image_paths, uid=111,username=111,create_time=now_str, update_time=now_str, heat=0)
        # 将新日记添加到日记列表中
        diaries.append(new_diary)
        # 将更新后的日记列表写入 JSON 文件
        Diary.write_diaries(diaries)

        return jsonify({'code': 200,'message': 'Diary published successfully', 'id': new_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 删除指定编号日记
@Diarybp.route('/api/diary/<int:diary_id>', methods=['DELETE'])
def DeleteDiary(diary_id):
    try:
        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()
        # 过滤掉要删除的日记，生成新的日记列表
        diaries = [diary for diary in diaries if diary.id != diary_id]
        # 将更新后的日记列表写入 JSON 文件
        Diary.write_diaries(diaries)

        return jsonify({"code": 200,'message': 'Diary deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 更新指定编号日记
@Diarybp.route('/api/diary/<int:id>', methods=['PUT'])
def UpadateDiary(id):
    try:
        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()
        # 获取前端传递的 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # 查找指定 id 的日记
        index = next((i for i, d in enumerate(diaries) if d.id == id), None)

        if index is not None:
            diary = diaries[index]
            title = data.get('title')
            content = data.get('content')
            image_paths = data.get('images', [])

            if title:
                diary.title = title
            if content:
                diary.content = content
            if image_paths:
                diary.images = image_paths

            # 获取当前时间
            now = datetime.datetime.now()
            now_str = now.strftime('%Y-%m-%d %H:%M:%S')

            diary.update_time = now_str

            # 更新日记列表中的对应日记
            diaries[index] = diary
            # 将更新后的日记列表写入 JSON 文件
            Diary.write_diaries(diaries)

            return jsonify({"code": 200,'message': 'Diary updated successfully'}), 200
        else:
            return jsonify({'error': 'Diary not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 获取指定编号日记
@Diarybp.route('/api/diary/<int:id>', methods=['GET'])
def GetDiary(id):
    try:
        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()
        # 查找指定编号的日记
        diary = next((diary for diary in diaries if diary.id == id), None)

        if diary:
            return jsonify(diary.model_dump()), 200
        else:
            return jsonify({'error': 'Diary not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 获取日记列表
@Diarybp.route('/api/diary', methods=['GET'])
def GetDiaryList():
    try:
        uid = request.args.get('uid', type=int)
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=3, type=int)
        if not uid and uid!=0:
            return jsonify({'error': 'No uid provided'}), 400

        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()
        # 过滤出指定 uid 的日记
        if uid and uid != 0:
            diaries = [diary for diary in diaries if diary.uid == uid]
        
        # 计算当前页起始索引
        start_index = (page - 1) * limit
        # 计算当前页结束索引
        end_index = start_index + limit
        # 获取当前页的日记数据
        paginated_diaries = diaries[start_index:end_index]

        # 构建响应数据字典
        response = {
            "diary_num": len(paginated_diaries),  # 当前页的日记数量
            # 将当前页的Diary对象转换为字典形式
            "data": [diary.model_dump() for diary in paginated_diaries],
            # 计算总页数
            "total_pages": (len(diaries) + limit - 1) // limit
        }
        # 将响应数据返回给客户端
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500