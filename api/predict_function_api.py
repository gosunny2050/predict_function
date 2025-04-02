from flask import Flask, Response, request, jsonify
import re
import json
import mysql.connector
from predict_by_model import classify_text
from function_config import fetch_function_details
from identify_argument import process_input

app = Flask(__name__)

# 配置数据库连接
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="abc123",
        password="abc123",
        database="predict"
    )

# 从数据库获取与 message 相似的函数信息
def get_function_info(message):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # 使用 MATCH ... AGAINST 进行相似度查询
    query = """
    SELECT function_name, argument_name, argument_detail
    FROM predict_function
    WHERE MATCH(function_description) AGAINST (%s IN NATURAL LANGUAGE MODE)
    ORDER BY MATCH(function_description) AGAINST (%s IN NATURAL LANGUAGE MODE) DESC
    LIMIT 1;
    """
    cursor.execute(query, (message, message))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    # 如果找到匹配的记录，返回函数名和参数
    if result:
        function_name = result['function_name']
        argument_name = result['argument_name']
        argument_detail = result['argument_detail']
        arguments = {argument_name: argument_detail} if argument_name and argument_detail else {}
        return True,function_name, argument_name
    else:
        # 若无匹配结果
        return False,"unknown", {}

@app.route('/predict/function', methods=['POST'])
def predict_function_api():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request, 'message' parameter is required"}), 400

    message = data['message']
    function_name = "unknow"
    arguments = {}
    # 获取函数名和参数
    matched,function_name, argument_name = get_function_info(message)
    if matched==False:
       index = classify_text(message)
       result = fetch_function_details(index)
       function_name = result["function_name"]
       argument_name = result["argument_name"]
    achieve_argument = process_input(function_name, message)
    if achieve_argument != None and argument_name!="":
       arguments[argument_name] = achieve_argument        
    # 格式化为 JSON 格式返回
    response = {
        "arguments":json.dumps(arguments, ensure_ascii=False),
        "function_name": function_name
    }
    return Response(
        json.dumps(response, ensure_ascii=False), 
        content_type='application/json; charset=utf-8'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

