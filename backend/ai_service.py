from typing import List
import os
import requests
import json

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-64f383dafe484e45a04919561a002db3"

class AIService:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_response(self, message: str, context: List[str] = None) -> str:
        """
        生成AI回复
        """
        try:
            # 构建提示词
            prompt = f"""
            你是一个专业的销售助手。请根据以下客户消息生成合适的回复：
            
            客户消息：{message}
            
            历史上下文：
            {self._format_context(context) if context else '无'}
            
            请生成专业、友好且有针对性的回复。
            """
            
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"抱歉，AI服务暂时不可用：{response.text}"
            
        except Exception as e:
            return f"抱歉，AI服务暂时不可用：{str(e)}"

    async def analyze_customer_intent(self, message: str) -> List[str]:
        """
        分析客户意图并推荐标签
        """
        try:
            prompt = f"""
            分析以下客户消息的意图，并推荐合适的标签（如：价格咨询、售后问题、产品咨询等）。
            请以JSON格式返回标签列表。
            
            客户消息：{message}
            """
            
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 200
            }
            
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                try:
                    # 尝试解析返回的JSON
                    return json.loads(content)
                except:
                    # 如果不是JSON格式，返回示例标签
                    return ["价格咨询", "产品咨询"]
            else:
                return []

        except Exception as e:
            return []

    def _format_context(self, context: List[str]) -> str:
        """
        格式化历史上下文
        """
        return "\n".join([f"- {msg}" for msg in context]) 