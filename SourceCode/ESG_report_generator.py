
url_file = input("请在此处输入报表网址：")
def get_file_from_url(url_file):
    import requests
    import io
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    req = requests.get(url_file, headers=send_headers)  # 通过访问互联网得到文件内容
    bytes_io = io.BytesIO(req.content)  # 转换为字节流
    with open('temp.pdf', 'wb') as file:
        file.write(bytes_io.getvalue())  # 保存到本地
    # import time
    # time.sleep(2) # 最好做一个休眠
    return bytes_io

get_file_from_url(url_file)



import pdfplumber  # 导入库
import jieba
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 用pdf文件解析器读取文件
with pdfplumber.open('temp.pdf') as f:
    # 用for循环读取文件中的每一页
    for page in f.pages:
        text = page.extract_text()
        txt_f = open(r'temp.txt', mode='a', encoding='utf-8')  # 创建txt文件
        txt_f.write(text)  # 写入txt文件

stopwords_file = 'dict.txt'  # 停用词文件路径

# 读取停用词文件，获取停用词集合
with open(stopwords_file, 'r', encoding='utf-8') as f:
    stopwords = set([line.strip() for line in f])

word_counts = {}  # 词频统计字典

with open('temp.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()  # 读取所有行

for line in lines:
    line = line.strip()  # 去除开头和结尾的空白符（包括换行符）
    if not line:  # 跳过空行
        continue
    words = jieba.lcut(line)  # 使用jieba库分词
    for word in words:
        if word not in stopwords:  # 如果不是停用词
            word_counts[word] = word_counts.get(word, 0) + 1  # 更新词频统计字典

# 打印词频统计结果
items = list(word_counts.items())
items.sort(key=lambda x: x[1], reverse=True)
y1 = []
labels = []
for i in range(1, 10):
    y1.append(items[i][1])
    labels.append(items[i][0])

width = 0.3
x = np.arange(len(y1))
a = [i for i in range(0, 9)]
plt.xticks(a, labels, rotation=30)
plt.bar(x=x, height=y1, width=width)
plt.title('文件中热词统计分析')
plt.savefig('热词柱状图.png')
plt.show()
print("热词统计分析完成")
stoplist = []
item = list(stopwords.items())
for i in range(len(item)):
    txt, counts = item[i]
    stoplist.append(txt)
print(stoplist)