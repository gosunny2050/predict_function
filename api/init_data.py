import csv
import pymysql
import json
from function_config import fetch_function_details

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "abc123",
    "password": "abc123",
    "database": "predict",
    "port": 3306,
    "charset": "utf8mb4"
}

# 文件路径
csv_file = "train_data.csv"

# 读取 CSV 文件
def load_data_from_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        return list(csvreader)
data = load_data_from_file(csv_file)
# 数据库操作
try:
    # 建立数据库连接
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 遍历 CSV 数据并插入数据库
    for row in data:
        function_description = row[0].strip()
        function_id = row[1].strip()
        result = fetch_function_details(function_id)
        function_name = result["function_name"]
        argument_name = result["argument_name"]
        # 插入语句
        insert_query = """
        INSERT INTO predict_function (function_id, function_name, function_description, argument_name)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (function_id, function_name, function_description, argument_name))

    # 提交事务
    connection.commit()

    print("数据插入成功！")

except Exception as e:
    print(f"发生错误: {e}")
    connection.rollback()

finally:
    # 关闭数据库连接
    if cursor:
        cursor.close()
    if connection:
        connection.close()

