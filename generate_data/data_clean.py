import os
import re

# 创建 result 文件夹，如果不存在
os.makedirs("result", exist_ok=True)

# 遍历 output_0.csv 到 output_38.csv 文件
for i in range(39):
    if i!=34:
       continue
    input_file_name = f"output_{i}_bak.csv"
    output_file_name = f"new_output_{i}_bak.csv"

    # 读取文件内容
    with open(input_file_name, "r", encoding="utf-8") as file:
        content = file.read()

    # 移除引号、数字和小数点
    cleaned_content = re.sub(r'["\d.]', '', content)

    # 去除空行和包含"批次："或"批次:"的行，并去重
    cleaned_lines = list({
        line for line in cleaned_content.splitlines()
        if line.strip() and "批次：" not in line and "批次:" not in line
    })

    # 将清理后的内容写入 result 文件夹中的新文件
    with open(output_file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(cleaned_lines))

