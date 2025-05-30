import sys

# 定义一个HuffNode虚类，里面包含两个虚方法：
# 1. 获取节点的权重函数
# 2. 获取此节点是否是叶节点的函数
class HuffNode(object):
    def get_wieght(self):
        # 此方法需要在子类中实现
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'get_wieght'")

    def isleaf(self):
        # 此方法需要在子类中实现
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'isleaf'")

# 树叶节点类
class LeafNode(HuffNode):
    # 初始化 树节点 需要初始化的对象参数有 ：value及其出现的频率freq
    def __init__(self, value=0, freq=0):
        super(LeafNode, self).__init__()
        # 节点的值
        self.value = value
        self.wieght = freq

    def isleaf(self):
        # 基类的方法，返回True，代表是叶节点
        return True

    def get_wieght(self):
        # 基类的方法，返回对象属性 weight，表示对象的权重
        return self.wieght

    def get_value(self):
        # 获取叶子节点的 字符 的值
        return self.value

# 中间节点类
class IntlNode(HuffNode):
    # 初始化 中间节点 需要初始化的对象参数有 ：left_child, right_chiled, weight
    def __init__(self, left_child=None, right_child=None):
        super(IntlNode, self).__init__()
        # 节点的值
        self.wieght = left_child.get_wieght() + right_child.get_wieght()
        # 节点的左右子节点
        self.left_child = left_child
        self.right_child = right_child

    def isleaf(self):
        # 基类的方法，返回False，代表是中间节点
        return False

    def get_wieght(self):
        # 基类的方法，返回对象属性 weight，表示对象的权重
        return self.wieght

    def get_left(self):
        # 获取左孩子
        return self.left_child

    def get_right(self):
        # 获取右孩子
        return self.right_child

# huffTree
class HuffTree(object):
    def __init__(self, flag, value =0, freq=0, left_tree=None, right_tree=None):
        super(HuffTree, self).__init__()
        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = IntlNode(left_tree.get_root(), right_tree.get_root())

    def get_root(self):
        # 获取huffman tree 的根节点
        return self.root

    def get_wieght(self):
        # 获取这个huffman树的根节点的权重
        return self.root.get_wieght()

    # 利用递归的方法遍历huffman_tree，并且以此方式得到每个 字符 对应的huffman编码
    # 保存在字典 char_freq中
    def traverse_huffman_tree(self, root, code, char_freq):
        if root.isleaf():
            char_freq[root.get_value()] = code
            return None
        else:
            self.traverse_huffman_tree(root.get_left(), code + '0', char_freq)
            self.traverse_huffman_tree(root.get_right(), code + '1', char_freq)

# 构造huffman树
def buildHuffmanTree(list_hufftrees):
    while len(list_hufftrees) > 1:
        # 1. 按照weight 对huffman树进行从小到大的排序
        list_hufftrees.sort(key=lambda x: x.get_wieght())
        # 2. 跳出weight 最小的两个huffman编码树
        temp1 = list_hufftrees[0]
        temp2 = list_hufftrees[1]
        list_hufftrees = list_hufftrees[2:]
        # 3. 构造一个新的huffman树
        newed_hufftree = HuffTree(1, 0, 0, temp1, temp2)
        # 4. 放入到数组当中
        list_hufftrees.append(newed_hufftree)
    # last.  数组中最后剩下来的那棵树，就是构造的Huffman编码树
    return list_hufftrees[0]

# 压缩文件，参数有 
# inputfilename：被压缩的文件的地址和名字
# outputfilename：压缩文件的存放地址和名字
def compress(inputfilename, outputfilename):
    # 1. 以二进制的方式打开文件 
    with open(inputfilename, 'rb') as f:
        filedata = f.read()
    # 获取文件的字节总数
    filesize = len(filedata)

    # 2. 统计 byte的取值［0-255］ 的每个值出现的频率
    # 保存在字典 char_freq中
    char_freq = {}
    for x in range(filesize):
        tem = filedata[x]
        if tem in char_freq.keys():
            char_freq[tem] = char_freq[tem] + 1
        else:
            char_freq[tem] = 1

    # 3. 开始构造原始的huffman编码树 数组，用于构造Huffman编码树
    list_hufftrees = []
    for x in char_freq.keys():
        # 使用 HuffTree的构造函数 定义一棵只包含一个叶节点的Huffman树
        tem = HuffTree(0, x, char_freq[x], None, None)
        # 将其添加到数组 list_hufftrees 当中
        list_hufftrees.append(tem)

    # 4. 步骤2中获取到的 每个值出现的频率的信息
    # 4.1. 保存叶节点的个数
    length = len(char_freq.keys())
    with open(outputfilename, 'wb') as output:
        # 一个int型的数有四个字节，所以将其分成四个字节写入到输出文件当中
        a4 = length & 255
        length = length >> 8
        a3 = length & 255
        length = length >> 8
        a2 = length & 255
        length = length >> 8
        a1 = length & 255
        output.write(bytes([a1]))
        output.write(bytes([a2]))
        output.write(bytes([a3]))
        output.write(bytes([a4]))

        # 4.2  每个值 及其出现的频率的信息
        # 遍历字典 char_freq
        for x in char_freq.keys():
            output.write(bytes([x]))
            # 
            temp = char_freq[x]
            # 同样出现的次数 是int型，分成四个字节写入到压缩文件当中
            a4 = temp & 255
            temp = temp >> 8
            a3 = temp & 255
            temp = temp >> 8
            a2 = temp & 255
            temp = temp >> 8
            a1 = temp & 255
            output.write(bytes([a1]))
            output.write(bytes([a2]))
            output.write(bytes([a3]))
            output.write(bytes([a4]))

    # 5. 构造huffman编码树，并且获取到每个字符对应的 编码
    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq)

    # 6. 开始对文件进行压缩
    code = ''
    with open(outputfilename, 'ab') as output:
        for i in range(filesize):
            key = filedata[i]
            code = code + char_freq[key]
            out = 0
            while len(code) > 8:
                for x in range(8):
                    out = out << 1
                    if code[x] == '1':
                        out = out | 1
                code = code[8:]
                output.write(bytes([out]))
                out = 0

        # 处理剩下来的不满8位的code
        output.write(bytes([len(code)]))
        out = 0
        for i in range(len(code)):
            out = out << 1
            if code[i] == '1':
                out = out | 1
        for i in range(8 - len(code)):
            out = out << 1
        # 把最后一位给写入到文件当中
        output.write(bytes([out]))

# 解压缩文件，参数有 
# inputfilename：压缩文件的地址和名字
# outputfilename：解压缩文件的存放地址和名字
def decompress(inputfilename, outputfilename):
    # 读取文件
    with open(inputfilename, 'rb') as f:
        filedata = f.read()
    # 获取文件的字节总数
    filesize = len(filedata)

    # 1. 读取压缩文件中保存的树的叶节点的个数
    # 一下读取 4个 字节，代表一个int型的值
    a1 = filedata[0]
    a2 = filedata[1]
    a3 = filedata[2]
    a4 = filedata[3]
    j = 0
    j = j | a1
    j = j << 8
    j = j | a2
    j = j << 8
    j = j | a3
    j = j << 8
    j = j | a4
    leaf_node_size = j

    # 2. 读取压缩文件中保存的相信的原文件中 ［0-255］出现的频率的信息
    # 构造一个 字典 char_freq 一遍重建 Huffman编码树
    char_freq = {}
    for i in range(leaf_node_size):
        c = filedata[4 + i * 5 + 0]
        a1 = filedata[4 + i * 5 + 1]
        a2 = filedata[4 + i * 5 + 2]
        a3 = filedata[4 + i * 5 + 3]
        a4 = filedata[4 + i * 5 + 4]
        j = 0
        j = j | a1
        j = j << 8
        j = j | a2
        j = j << 8
        j = j | a3
        j = j << 8
        j = j | a4
        char_freq[c] = j

    # 3. 重建huffman 编码树，和压缩文件中建立Huffman编码树的方法一致
    list_hufftrees = []
    for x in char_freq.keys():
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)
    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq)

    # 4. 使用步骤3中重建的huffman编码树，对压缩文件进行解压缩
    with open(outputfilename, 'wb') as output:
        code = ''
        currnode = tem.get_root()
        for x in range(leaf_node_size * 5 + 4, filesize):
            c = filedata[x]
            for i in range(8):
                if c & 128:
                    code = code + '1'
                else:
                    code = code + '0'
                c = c << 1

            while len(code) > 24:
                if currnode.isleaf():
                    tem_byte = bytes([currnode.get_value()])
                    output.write(tem_byte)
                    currnode = tem.get_root()
                if code[0] == '1':
                    currnode = currnode.get_right()
                else:
                    currnode = currnode.get_left()
                code = code[1:]

        # 4.1 处理最后 24位
        sub_code = code[-16:-8]
        last_length = 0
        for i in range(8):
            last_length = last_length << 1
            if sub_code[i] == '1':
                last_length = last_length | 1
        code = code[:-16] + code[-8:-8 + last_length]
        while len(code) > 0:
            if currnode.isleaf():
                tem_byte = bytes([currnode.get_value()])
                output.write(tem_byte)
                currnode = tem.get_root()
            if code[0] == '1':
                currnode = currnode.get_right()
            else:
                currnode = currnode.get_left()
            code = code[1:]
        if currnode.isleaf():
            tem_byte = bytes([currnode.get_value()])
            output.write(tem_byte)
            currnode = tem.get_root()