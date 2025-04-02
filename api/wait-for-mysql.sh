#!/bin/bash
set -e

# 等待 MySQL 服务启动
echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h "127.0.0.1" --silent; do
    sleep 1
done

echo "MySQL is ready!"

