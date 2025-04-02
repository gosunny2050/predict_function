# Start with a lightweight base image
FROM python:3.8-slim

# Set environment to non-interactive for faster installations
ENV DEBIAN_FRONTEND=noninteractive

# Install required system packages, set timezone, and install Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales tzdata lrzsz && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    locale-gen zh_CN.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip3 install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --timeout=100 \
    torch==2.0.1 -f https://download.pytorch.org/whl/cpu.html -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install --no-cache-dir transformers pandas scikit-learn tqdm -i https://pypi.tuna.tsinghua.edu.cn/simple

# Set language environment to Chinese UTF-8
ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

# Set working directory in container
WORKDIR /app

# Copy current directory contents into container
COPY . /app

# Set environment variable to ensure CPU usage only
ENV CUDA_VISIBLE_DEVICES=""

# Specify the command to run on container start
CMD ["python3", "train_model.py"]

