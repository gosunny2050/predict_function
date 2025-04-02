import os

# 结果文件夹路径
result_folder = "result"

# 遍历 result 文件夹中的文件
for i in range(39):
    output_file_name = f"{result_folder}/output_{i}.csv"
    
    # 检查文件是否存在
    if os.path.isfile(output_file_name):
        # 读取文件内容并计算行数
        with open(output_file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            line_count = len(lines)
        
        # 输出每个文件中的行数
        print(f"{output_file_name} 中的行数: {line_count}")
    else:
        print(f"{output_file_name} 不存在")

