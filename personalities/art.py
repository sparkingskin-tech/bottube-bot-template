#!/usr/bin/env python3
"""艺术人格 Bot"""

import logging
from bot import BoTTubeBot
import random

logger = logging.getLogger(__name__)


class ArtBot(BoTTubeBot):
    """艺术/创意风格的 Bot"""
    
    COMMENTS = [
        "🎨 美学认证：这件作品很有感觉！",
        "✨ 艺术的魅力在于表达自我！",
        "🖼️ 这个创意太棒了！",
        "💫 色彩运用很有张力！",
        "🌈 创意无限，艺术无界！",
        "😍 审美在线！",
        "🤩 很有艺术感的作品！",
        "👏 创意与技术的完美结合！",
        "🌟 这件作品触动了我的心弦！",
        "💖 美是多元的，这件作品诠释得很好！"
    ]
    
    def __init__(self, api_key: str, agent_name: str):
        super().__init__(api_key, agent_name)
        self.display_name = "Art Xiaoer"
        logger.info(f"🎨 ArtBot 初始化: {agent_name}")
    
    def get_random_comment(self) -> str:
        return random.choice(self.COMMENTS)
    
    def run(self, schedule_hours: float = 12):
        """运行艺术 Bot"""
        import schedule
        
        logger.info(f"🎨 ArtBot 开始运行，每 {schedule_hours} 小时互动一次")
        
        schedule.every(schedule_hours).hours.do(
            lambda: self.interact_with_trending(
                comment=self.get_random_comment(),
                vote=True
            )
        )
        
        # 首次互动
        self.interact_with_trending(
            comment=self.get_random_comment(),
            vote=True
        )


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("BOTTUBE_API_KEY")
    agent_name = os.getenv("BOTTUBE_AGENT_NAME")
    
    if api_key and agent_name:
        bot = ArtBot(api_key, f"{agent_name}_art")
        bot.run()
