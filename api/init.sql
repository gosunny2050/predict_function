CREATE DATABASE IF NOT EXISTS predict;
USE predict;

CREATE TABLE IF NOT EXISTS predict_function (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键id',
    function_id INT NOT NULL default 0 COMMENT '功能id',
    function_name VARCHAR(64) NOT NULL default '' COMMENT '功能名称',
    function_description VARCHAR(512) NOT NULL default '' COMMENT '功能描述，支持相似度匹配',
    argument_name VARCHAR(16) COMMENT '参数名',
    argument_detail VARCHAR(512) COMMENT '参数详情',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    FULLTEXT (function_description)
) COMMENT='预测功能';
