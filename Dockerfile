FROM python:3.11-slim

WORKDIR /app

# 安装 ffmpeg (视频处理需要)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建视频目录
RUN mkdir -p videos

# 设置权限
RUN chmod +x bot.py

# 默认命令
CMD ["python", "bot.py"]
