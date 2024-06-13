# 读取json文件
import json
with open('output.json', 'r') as file:
    res = json.load(file)
    print(type(res))

# 获取res中的"result"
print(type(res['result']))

# 获取list长度
print(len(res['result']))