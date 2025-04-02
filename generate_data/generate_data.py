import csv
import time
from openai import OpenAI

client = OpenAI(
     api_key="xxx",
    base_url="xxx"
)

# 流式响应
def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)"""
    response_content = ""
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content += chunk.choices[0].delta.content
    return response_content

def process_contents(input_file: str, output_file: str, batch_size=90):
    """从文件中读取内容，调用 GPT-3.5 生成 10000 个类似短句，并写入 CSV 文件。

    Args:
        input_file (str): 输入文件路径，每一行为一个 content。
        output_file (str): 输出 CSV 文件路径。
        batch_size (int): 每次生成多少个短句，默认1000。
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        # 循环读取每一行内容
        for index, line in enumerate(file):
            if index !=34:
                continue
            index_str = str(index)
            output_path = f"{output_file}_{index_str}.csv"
            with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                content = line.strip()
                print(content, index)
                if content:
                    total_generated = 0  # 记录已生成的短句总数
                    # 批次生成，直到生成总计 10,000 个类似短语
                    for batch in range(0, 10000, batch_size):
                        try:
                            # 生成提示
                            messages = [{'role': 'user', 'content': f"请生成和'{content}'类似的短句，批次 {batch // batch_size + 1}，每批 {batch_size} 个"}]
                            # 调用 GPT-3.5 API 生成一批内容
                            generated_content = gpt_35_api_stream(messages).replace('"', '').strip()

                            # 检查生成内容是否为空
                            if not generated_content:
                                print(f"批次 {batch // batch_size + 1} 返回空内容，跳过")
                                continue

                            # 将生成的内容分成每行独立的短句
                            lines = generated_content.splitlines()
                            lines = [line for line in lines if line.strip()]  # 去掉空行
                            csv_writer.writerows([[line] for line in lines])  # 写入每行
                            
                            # 更新已生成短句总数
                            total_generated += len(lines)
                            print(f"批次 {batch // batch_size + 1} 完成，共生成 {len(lines)} 行")

                            # 延时1秒，避免频繁请求
                            time.sleep(1)

                            # 提前检查是否达到 10000 行
                            if total_generated >= 10000:
                                print(f"{output_path} 达到 10,000 行，提前结束")
                                break

                        except Exception as e:
                            print(f"批次 {batch // batch_size + 1} 生成失败: {e}")
                            time.sleep(5)
                            continue
                            
                # 输出文件总行数，检查生成情况
                with open(output_path, 'r', encoding='utf-8') as f:
                    total_lines = sum(1 for _ in f)
                    print(f"{output_path} 总行数：{total_lines}")
                    if total_lines < 10000:
                        print(f"{output_path} 文件行数未达到 10,000 行，实际行数为：{total_lines}")
                    else:
                        print(f"{output_path} 文件行数已达到 10,000 行")


if __name__ == '__main__':
    input_file = '/xxx/Downloads/data/input.csv'  # 输入文件，每一行为一个 content
    output_file = 'repair/new_output'  # 输出文件，保存生成的内容和索引
    process_contents(input_file, output_file)


