FROM mariadb:10.5

# 复制初始化 SQL 脚本
COPY init.sql /docker-entrypoint-initdb.d/
# 复制自定义配置文件
COPY custom.cnf /etc/mysql/conf.d/

# 设置 MySQL 环境变量
ENV MYSQL_DATABASE=predict \
    MYSQL_USER=abc123 \
    MYSQL_PASSWORD=abc123 \
    MYSQL_ROOT_PASSWORD=abc123

# 安装 Python 和依赖
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 Python 库
RUN pip3 install --no-cache-dir flask pymysql mysql-connector-python torch torchvision transformers

# 设置工作目录
WORKDIR /app

# 复制应用文件
COPY . /app

# 暴露端口
EXPOSE 3306 5000

# 启动服务
CMD ["sh", "-c", "docker-entrypoint.sh mysqld & /app/wait-for-mysql.sh && python3 /app/init_data.py && python3 /app/predict_function_api.py"]

