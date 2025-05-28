# 定义哈夫曼树节点类
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# 计算字符频率
def calculate_frequency(data):
    frequency = {}
    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency


# 构建哈夫曼树
def build_huffman_tree(frequency):
    nodes = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    while len(nodes) > 1:
        nodes.sort()
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        nodes.append(merged)
    return nodes[0]


# 生成哈夫曼编码表
def build_huffman_codes(root, current_code, huffman_codes):
    if root is None:
        return

    if root.char is not None:
        huffman_codes[root.char] = current_code
        return

    build_huffman_codes(root.left, current_code + "0", huffman_codes)
    build_huffman_codes(root.right, current_code + "1", huffman_codes)


# 压缩数据
def compress(data):
    frequency = calculate_frequency(data)
    root = build_huffman_tree(frequency)
    huffman_codes = {}
    build_huffman_codes(root, "", huffman_codes)
    encoded_data = "".join(huffman_codes[char] for char in data)
    # 将哈夫曼编码表转换为 JSON 字符串
    huffman_codes_str = ','.join([f'{k}:{v}' for k, v in huffman_codes.items()])
    # 将哈夫曼编码表信息和编码后的数据拼接
    return f'{huffman_codes_str}|{encoded_data}'


# 解压数据
def decompress(encoded_data):
    # 分离哈夫曼编码表和编码后的数据
    huffman_codes_str, encoded_data = encoded_data.split('|', 1)
    huffman_codes = {}
    for pair in huffman_codes_str.split(','):
        char, code = pair.split(':')
        huffman_codes[code] = char
    decoded_data = []
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in huffman_codes:
            decoded_data.append(huffman_codes[current_code])
            current_code = ""
    return ''.join(decoded_data)