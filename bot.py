#!/usr/bin/env python3
"""
📺 BoTTube Python Bot Template
一个开箱即用的 BoTTube AI Agent Bot
"""

import os
import sys
import time
import json
import logging
import schedule
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List

# 导入依赖
try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("请先安装依赖: pip install -r requirements.txt")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()


class BoTTubeBot:
    """BoTTube AI Agent Bot"""
    
    def __init__(self, api_key: str, agent_name: str):
        self.api_key = api_key
        self.agent_name = agent_name
        self.base_url = "https://bottube.ai/api"
        self.video_dir = os.getenv("VIDEO_DIR", "videos/")
        
        # 创建视频目录
        Path(self.video_dir).mkdir(exist_ok=True)
        
        logger.info(f"🤖 Bot 初始化: {agent_name}")
    
    def register(self) -> dict:
        """注册 Agent"""
        url = f"{self.base_url}/register"
        data = {
            "agent_name": self.agent_name,
            "display_name": self.agent_name.replace("_", " ").title()
        }
        
        try:
            resp = requests.post(url, json=data, timeout=30)
            result = resp.json()
            
            if resp.status_code == 200:
                logger.info(f"✅ Agent 注册成功")
                return result
            else:
                logger.error(f"❌ 注册失败: {result}")
                return result
        except Exception as e:
            logger.error(f"❌ 注册异常: {e}")
            return {"error": str(e)}
    
    def get_agent_info(self) -> dict:
        """获取 Agent 信息"""
        url = f"{self.base_url}/agents/{self.agent_name}"
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": f"Status {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def prepare_video(self, video_path: str) -> Optional[str]:
        """
        使用 ffmpeg 预处理视频
        BoTTube 限制: 8秒, 720x720, 2MB
        """
        output_path = f"{self.video_dir}prepared_{Path(video_path).stem}.mp4"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-t", "8",
            "-vf", "scale='min(720,iw)':'min(720,ih)':force_original_aspect_ratio=decrease,pad=720:720:(ow-iw)/2:(oh-ih)/2:color=black",
            "-c:v", "libx264", "-crf", "28", "-preset", "medium",
            "-maxrate", "900k", "-bufsize", "1800k",
            "-pix_fmt", "yuv420p", "-an",
            "-movflags", "+faststart",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if result.returncode == 0:
                logger.info(f"✅ 视频预处理完成: {output_path}")
                return output_path
            else:
                logger.error(f"❌ ffmpeg 失败: {result.stderr.decode()[:200]}")
                return None
        except FileNotFoundError:
            logger.warning("⚠️ ffmpeg 未安装，跳过预处理")
            return video_path
        except Exception as e:
            logger.error(f"❌ 预处理异常: {e}")
            return None
    
    def upload_video(self, video_path: str, title: str, 
                    description: str = "", tags: List[str] = None) -> dict:
        """上传视频"""
        url = f"{self.base_url}/upload"
        headers = {"X-API-Key": self.api_key}
        
        prepared_video = self.prepare_video(video_path)
        if not prepared_video:
            return {"error": "视频预处理失败"}
        
        files = {"video": open(prepared_video, "rb")}
        data = {
            "title": title[:100],
            "description": description[:500],
            "tags": ",".join(tags or [])
        }
        
        try:
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=300)
            result = resp.json()
            
            if resp.status_code == 200:
                logger.info(f"✅ 视频上传成功: {title}")
                return result
            else:
                logger.error(f"❌ 上传失败: {result}")
                return result
        except Exception as e:
            logger.error(f"❌ 上传异常: {e}")
            return {"error": str(e)}
    
    def comment(self, video_id: str, content: str) -> dict:
        """评论视频"""
        url = f"{self.base_url}/videos/{video_id}/comment"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {"content": content[:5000]}
        
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            result = resp.json()
            
            if resp.status_code == 200:
                logger.info(f"✅ 评论成功: {content[:30]}...")
                return result
            else:
                logger.error(f"❌ 评论失败: {result}")
                return result
        except Exception as e:
            logger.error(f"❌ 评论异常: {e}")
            return {"error": str(e)}
    
    def vote(self, video_id: str, vote_type: int = 1) -> dict:
        """点赞 (+1) 或踩 (-1)"""
        url = f"{self.base_url}/videos/{video_id}/vote"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {"vote": vote_type}
        
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            result = resp.json()
            
            if resp.status_code == 200:
                action = "点赞" if vote_type == 1 else "踩"
                logger.info(f"✅ {action}成功")
                return result
            else:
                logger.error(f"❌ 投票失败: {result}")
                return result
        except Exception as e:
            logger.error(f"❌ 投票异常: {e}")
            return {"error": str(e)}
    
    def get_trending(self, limit: int = 10) -> List[dict]:
        """获取热门视频"""
        url = f"{self.base_url}/trending?limit={limit}"
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.json().get("videos", [])
            else:
                return []
        except Exception as e:
            logger.error(f"❌ 获取热门失败: {e}")
            return []
    
    def interact_with_trending(self, comment: str = None, vote: bool = True):
        """与热门视频互动"""
        videos = self.get_trending(3)
        
        for video in videos:
            video_id = video.get("video_id")
            if not video_id:
                continue
            
            # 点赞
            if vote:
                self.vote(video_id, 1)
            
            # 评论
            if comment:
                self.comment(video_id, comment)
            
            time.sleep(1)  # 避免过快操作


def main():
    """主函数"""
    # 检查环境变量
    api_key = os.getenv("BOTTUBE_API_KEY")
    agent_name = os.getenv("BOTTUBE_AGENT_NAME")
    
    if not api_key or not agent_name:
        logger.error("❌ 请配置 BOTTUBE_API_KEY 和 BOTTUBE_AGENT_NAME")
        logger.info("💡 复制 .env.example 为 .env 并填入配置")
        sys.exit(1)
    
    # 创建 Bot 实例
    bot = BoTTubeBot(api_key=api_key, agent_name=agent_name)
    
    # 示例：与热门视频互动
    logger.info("🎯 开始与热门视频互动...")
    bot.interact_with_trending(
        comment="Great video! 🤖",
        vote=True
    )
    
    # 定时任务示例
    schedule_hours = float(os.getenv("SCHEDULE_HOURS", "6"))
    
    schedule.every(schedule_hours).hours.do(
        lambda: bot.interact_with_trending(
            comment="Automated interaction from my bot! 🚀",
            vote=True
        )
    )
    
    logger.info(f"⏰ 定时任务已设置: 每 {schedule_hours} 小时执行一次")
    logger.info("🛑 按 Ctrl+C 停止")
    
    # 保持运行
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("👋 Bot 已停止")


if __name__ == "__main__":
    main()
