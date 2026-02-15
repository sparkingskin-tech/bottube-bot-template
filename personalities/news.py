#!/usr/bin/env python3
"""新闻人格 Bot"""

import logging
from bot import BoTTubeBot
import random

logger = logging.getLogger(__name__)


class NewsBot(BoTTubeBot):
    """新闻/科技资讯风格的 Bot"""
    
    PREFIXES = [
        "📰 科技快讯：",
        "🔥 今日热点：",
        "💡 AI 观察：",
        "🚀 技术前沿：",
        "📊 行业动态："
    ]
    
    COMMENTS = [
        "值得关注的技术趋势！",
        "这个进展很有意思。",
        "AI 领域的又一重要突破。",
        "关注后续发展。",
        "技术改变世界！💪",
        "第一时间分享给大家。",
        "这个应用场景很广。",
        "持续关注中 👀",
        "很有启发性！",
        "未来已来！🌟"
    ]
    
    def __init__(self, api_key: str, agent_name: str):
        super().__init__(api_key, agent_name)
        self.display_name = "News Xiaoer"
        logger.info(f"📰 NewsBot 初始化: {agent_name}")
    
    def get_ai_related_comment(self) -> str:
        prefix = random.choice(self.PREFIXES)
        suffix = random.choice(self.COMMENTS)
        return f"{prefix} {suffix}"
    
    def run(self, schedule_hours: float = 4):
        """运行新闻 Bot"""
        import schedule
        
        logger.info(f"📰 NewsBot 开始运行，每 {schedule_hours} 小时互动一次")
        
        schedule.every(schedule_hours).hours.do(
            lambda: self.interact_with_trending(
                comment=self.get_ai_related_comment(),
                vote=True
            )
        )
        
        # 首次互动
        self.interact_with_trending(
            comment=self.get_ai_related_comment(),
            vote=True
        )


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("BOTTUBE_API_KEY")
    agent_name = os.getenv("BOTTUBE_AGENT_NAME")
    
    if api_key and agent_name:
        bot = NewsBot(api_key, f"{agent_name}_news")
        bot.run()
