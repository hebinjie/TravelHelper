import json
import os
from typing import List
from flask import Blueprint, request, jsonify,g
from models.diary import Diary
import datetime
from routes.user import token_required
from models.method import sort_data,recommend_data, search_diaries

# 创建蓝图对象，用于组织路由
Diarybp = Blueprint('diary', __name__)

# 发布日记
@Diarybp.route('/api/diary', methods=['POST'])
@token_required
def CreateDiary():
    try:
        # # 获取当前文件的绝对路径
        # current_file_path = os.path.abspath(__file__)
        # current_dir = os.path.dirname(current_file_path)

        # # 构建目标文件的相对路径
        # json_file_path = os.path.join(current_dir, "..", "generated_diaries.json")

        # # 读取生成的 JSON 文件
        # with open(json_file_path, "r") as f:
        #     diaries_data = json.load(f)

        # # 转换为 Diary 对象列表
        # diaries: List[Diary] = [Diary(**item) for item in diaries_data]

        # # 写入压缩文件
        # Diary.write_diaries(diaries)

        # # 从压缩文件读取
        # loaded_diaries = Diary.read_diaries()
        # print(f"成功加载 {len(loaded_diaries)} 篇日记")
        # return jsonify({'code': 200,'message': 'Diary published successfully', 'id': 1}), 200


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
        
        # 从 g 对象中获取 username 和 uid
        username = g.user.get('username')
        uid = g.user.get('uid')

        # 创建新的日记对象
        new_diary = Diary(id=new_id, title=title, content=content, images=image_paths, uid=uid,username=username,create_time=now_str, update_time=now_str, heat=0, rate=0, rate_num=0, tags=[])
        # 将新日记添加到日记列表中
        diaries.append(new_diary)
        # 将更新后的日记列表写入 JSON 文件
        Diary.write_diaries(diaries)

        return jsonify({'code': 200,'message': 'Diary published successfully', 'id': new_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除指定编号日记
@Diarybp.route('/api/diary/<int:diary_id>', methods=['DELETE'])
@token_required
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
@token_required
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
@token_required
def GetDiary(id):
    try:
        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()
        # 查找指定编号的日记
        diary = next((diary for diary in diaries if diary.id == id), None)

        if diary:
            diary.heat += 1  # 增加热度
            # 将更新后的日记列表写入 JSON 文件
            Diary.write_diaries(diaries)
            return jsonify(diary.model_dump()), 200
        else:
            return jsonify({'error': 'Diary not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取日记列表
@Diarybp.route('/api/diary', methods=['GET'])
@token_required
def ListDiaries():
    try:
        s = request.args.getlist('s')
        uid = request.args.get('uid', type=int)
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=3, type=int)
        sortby= request.args.get('sortby', default='heat', type=str)  # 获取排序方式，默认为热度排序
        method= request.args.get('method', default='desc', type=str)  # 获取排序方法，默认为降序
        filter = request.args.get('filter', default='all', type=str)  # 获取过滤方式，默认为全部
        reader_id = g.user.get('uid')
        if not uid and uid!=0:
            return jsonify({'error': 'No uid provided'}), 400
        
        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()

        if s:
            # 调用搜索函数
            diaries = search_diaries(diaries, s)
        # 过滤出指定 uid 的日记
        if uid and uid != 0:
            diaries = [diary for diary in diaries if diary.uid == uid]
        if filter and filter != 'all':
            # 过滤出指定类型的日记
            diaries = [diary for diary in diaries if diary.type == filter]
        
        count = len(diaries)  # 计算符合条件的日记数量

        if sortby:
            # 按指定属性进行排序
            if sortby == 'time':
                diaries = sort_data(diaries, 'create_time', method)
            elif sortby == 'recommend':
                diaries = recommend_data(diaries, reader_id)  # 调用推荐函数进行排序
            else:
                diaries= sort_data(diaries, sortby, method)
        
        # 错误页码
        if page < 1:
            return jsonify({'error': 'Invalid page number'}), 400
        # 计算当前页起始索引
        start_index = (page - 1) * limit
        # 计算当前页结束索引
        end_index = start_index + limit
        # 获取当前页的日记数据
        paginated_diaries = diaries[start_index:end_index]

        # 构建响应数据字典
        response = {
            "diary_num": count,  # 日记总数量
            # 将当前页的Diary对象转换为字典形式
            "data": [{**diary.model_dump(), 
                    "content": diary.content[:20]} for diary in paginated_diaries],
            # 计算总页数
            "total_pages": (len(diaries) + limit - 1) // limit
        }
        # 将响应数据返回给客户端
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 评价日记接口
@Diarybp.route('/api/diary/<int:id>', methods=['POST'])
@token_required
def JudgeDiary(id):
    try:
        # 从 JSON 文件中读取日记数据
        diaries = Diary.read_diaries()
        # 获取前端传递的 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        # 从 JSON 数据中获取日记评分
        rate = data.get('rate')

        if not id:
            return jsonify({'error': 'No ID provided'}), 400
        
        # 查找指定 id 的日记
        index = next((i for i, d in enumerate(diaries) if d.id == id), None)

        if index is not None:
            diary = diaries[index]

            diary.rate = (diary.rate * diary.rate_num + rate) / (diary.rate_num + 1) if diary.rate_num > 0 else rate
            diary.rate_num += 1

            # 更新日记列表中的对应日记
            diaries[index] = diary
            # 将更新后的日记列表写入 JSON 文件
            Diary.write_diaries(diaries)

            return jsonify({"code": 200,'message': 'Diary Judged successfully'}), 200
        else:
            return jsonify({'error': 'Diary not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500