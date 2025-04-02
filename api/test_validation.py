import requests
import json

# 配置接口 URL 和头部信息
url = "http://10.45.62.78/predict/function"
headers = {
    "Host": "butter-staging1.baidu-int.com",
    "Content-Type": "application/json"
}

# 输入文件路径
input_file = "validation.txt"

# 逐行读取文件并调用接口
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        message = line.strip()  # 去除行尾换行符或空格
        if not message:
            continue  # 跳过空行
        
        # 构造请求数据
        payload = {
            "message": message
        }

        try:
            # 调用接口
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            # 检查响应状态码并输出结果
            if response.status_code == 200:
                print(f"Message '{message}' 处理成功: {response.text}")
            else:
                print(f"Message '{message}' 请求失败，状态码: {response.status_code}, 响应: {response.text}")
        except Exception as e:
            print(f"调用接口时出错: {e}")
