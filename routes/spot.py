from flask import Blueprint, request, jsonify
from models.spot import Spot
from models.method import sort_data

# 创建蓝图对象，用于组织路由
Spotbp = Blueprint('spot', __name__)

# 获取景点列表
@Spotbp.route('/api/spots', methods=['GET'])
def GetSpots():
    try:
        page=request.args.get('page', default=1, type=int)  # 获取页码，默认为1
        limit=request.args.get('limit', default=3, type=int)
        sortby=request.args.get('sortby', default='heat', type=str)  # 获取排序方式，默认为热度排序
        method=request.args.get('method', default='asc', type=str)  # 获取排序方法，默认为升序
        s= request.args.getlist('s')  # 获取搜索关键词

        if not page or not limit:
            return jsonify({'error': 'No page or limit provided'}), 400
        
        spots= Spot.read_spots()  # 从 JSON 文件中读取景点数据

        if s:
            # 过滤出包含关键词的景点
            spots = [spot for spot in spots if any(keyword in spot.name + spot.description for keyword in s)]
        
        if sortby:
            # 按指定属性进行排序
            spots= sort_data(spots, sortby, method)

        start= (page - 1) * limit  # 计算当前页起始索引
        end= start + limit  # 计算当前页结束索引
        paginated_spots= spots[start:end]

        response= {
            "code": 200,
            "spots": [{**spot.model_dump()} for spot in paginated_spots], # 将当前页的Spot对象转换为字典形式
            "total_pages": (len(spots) + limit - 1) // limit  # 计算总页数
        }

        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500