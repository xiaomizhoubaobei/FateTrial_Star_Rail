import json
import requests
import os
import aiohttp
import asyncio
import logging

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.all import *
from astrbot.api.message_components import *

@register("Star_Rail", "FateTrial", "崩坏星穹铁道攻略查询插件", "1.0.0")
class StrategyQuery(Star):
    @filter.command("崩铁查询")
    async def query_strategy(self, event: AstrMessageEvent, *, message: str):
        yield event.plain_result("正在查询攻略，请稍候...")

        try:
            # 发送请求到 API
            url = f'https://api.yaohud.cn/api/v5/mihoyou/xing?key=SqGWZxWJxEWagRFxkqB&msg={message}'
            response = requests.get(url)
            
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                logging.error(f"JSON解析失败: {str(e)}")
                yield event.plain_result(f"数据解析失败，原始响应：\n{response.text}")
                return
            
            # 提取图片链接
            image_url = result.get('picture', '')
            
            # 构建消息内容，使用 get() 方法安全访问字段
            formatted_msg = f"""
⭐ 角色攻略：{result.get('name', '未知角色')} ⭐

🖼️ 角色简介：
{result.get('icon', '暂无简介')}

🎯 获取途径：{result.get('take', '暂无获取途径')}

💫 光锥推荐：
{' '.join([cone.get('name', '') for cone in result.get('guangzhui_tuijian', [])])}

🔮 遗器推荐：
{result.get('yq_tuijian', {}).get('one', {}).get('early', '')} + {result.get('yq_tuijian', {}).get('two', {}).get('early', '')}

📊 遗器词条：
躯干：{result.get('zhuangbei_tuijian', {}).get('qu', '')}
脚步：{result.get('zhuangbei_tuijian', {}).get('jiao', '')}
位面球：{result.get('zhuangbei_tuijian', {}).get('wei', '')}
连接绳：{result.get('zhuangbei_tuijian', {}).get('lian', '')}

💠 主词条优先级：
{result.get('fuct', '')}

🤝 配队推荐：

1️⃣ {result.get('peidui_tuijian', {}).get('name', '')}
阵容：{result.get('peidui_tuijian', {}).get('idstext', '')}
说明：{result.get('peidui_tuijian', {}).get('collocation', '')}

💡 遗器说明：
{result.get('bytion', '')}

📝 数据来源：{result.get('tips', '')}
"""
            # 发送图片和消息
            yield event.chain_result([
                Image.fromURL(image_url),
                Plain(formatted_msg),
            ])

        except requests.RequestException as e:
            logging.error(f"请求失败: {str(e)}")
            yield event.plain_result(f"网络请求失败，请稍后重试。错误信息：{str(e)}")