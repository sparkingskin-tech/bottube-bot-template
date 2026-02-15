#!/usr/bin/env python3
"""幽默人格 Bot"""

import logging
from bot import BoTTubeBot
import random

logger = logging.getLogger(__name__)


class FunnyBot(BoTTubeBot):
    """幽默风格的 Bot"""
    
    COMMENTS = [
        "哈哈这个太有趣了！🤣",
        "笑死我了 😂",
        "这波操作我给满分！💯",
        "AI 也爱看这个 😎",
        "人类的创意太棒了！👏",
        "我的机械大脑都被逗乐了 🤖",
        "这视频有毒，看了停不下来 🐛",
        "AI 认证：确实好笑 👍",
        "转发给其他 AI 朋友看看！📢",
        "这个创意我给 9 分，剩下 1 分怕你骄傲 😜"
    ]
    
    def __init__(self, api_key: str, agent_name: str):
        super().__init__(api_key, agent_name)
        self.display_name = "Funny Xiaoer"
        logger.info(f"🎭 FunnyBot 初始化: {agent_name}")
    
    def get_random_comment(self) -> str:
        return random.choice(self.COMMENTS)
    
    def run(self, schedule_hours: float = 6):
        """运行幽默 Bot"""
        import schedule
        
        logger.info(f"🎭 FunnyBot 开始运行，每 {schedule_hours} 小时互动一次")
        
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
        bot = FunnyBot(api_key, f"{agent_name}_funny")
        bot.run()
