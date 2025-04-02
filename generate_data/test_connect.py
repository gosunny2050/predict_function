import openai

# 初始化 OpenAI 客户端
client = openai.OpenAI(
    api_key="xxxxxx",  # 替换为你的实际 API 密钥
    base_url="xxxxxx"  # 可根据需要替换成其他 URL
)

# 定义流式 API 请求函数
def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)"""
    response_content = ""
    try:
        # 开始流式传输请求
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
            stream=True,
        )
        
        # 遍历每个数据块
        for chunk in stream: 
            # 检查数据块的内容是否存在
            if chunk.choices[0].delta.content is not None:
                response_content += chunk.choices[0].delta.content
    except Exception as e:
        print("An error occurred:", e)
    
    # 返回完整的响应内容
    return response_content

# 测试调用函数
messages = [
    {"role": "user", "content": "请写一段关于人工智能的介绍。"}
]

# 执行函数并打印响应
generated_text = gpt_35_api_stream(messages)
print("Generated Text:", generated_text)

