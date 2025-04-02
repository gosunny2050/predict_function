import os

# 定义文件路径
old_path = "/xxxxxx/old/result"
new_path = "/xxxxxx/new/result"
merge_path = "/xxxxxx/merge_result"

# 创建合并后的文件夹（如果不存在）
os.makedirs(merge_path, exist_ok=True)

# 遍历文件并一一对应合并
for i in range(39):
    old_file = os.path.join(old_path, f"output_{i}.csv")
    new_file = os.path.join(new_path, f"new_output_{i}.csv")
    merge_file = os.path.join(merge_path, f"merge_output_{i}.csv")
    
    # 读取两个文件的内容
    with open(old_file, 'r') as f_old, open(new_file, 'r') as f_new:
        old_lines = f_old.readlines()
        new_lines = f_new.readlines()

    # 合并内容并去重
    merged_lines = list(set(old_lines + new_lines))

    # 写入合并后的文件
    with open(merge_file, 'w') as f_merge:
        f_merge.writelines(merged_lines)

print("文件合并完成并去重！")

