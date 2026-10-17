import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from src.data_loader import load_data
from src.tools import get_tool_result
from src.memory import MemoryManager

# 1. 环境与初始化
load_dotenv()
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"), 
    base_url=os.getenv("LLM_BASE_URL")
)
MODEL_NAME = os.getenv("LLM_MODEL_NAME", "qwen-max")
memory_mgr = MemoryManager()

def build_system_prompt(persona, user_id="1"):
    """
    【核心升级】：将画像和记忆注入 System Prompt
    """
    player_profile = memory_mgr.get_player_profile(user_id)
    chat_history = memory_mgr.load_memory()
    
    return f"""
    {persona}
    
    【当前玩家档案】
    {player_profile}
    
    【之前的聊天记忆】
    {chat_history}
    
    要求：
    1. 你是 GamePilot，一个懂游戏的 AI 伙伴。
    2. 无论在什么模式下，都要自然地结合玩家画像进行回复。
    3. 语气亲切，像资深游戏好友。
    """

def ask_agent(question, persona="分析模式", mode="analysis"):
    user_id = "1" 
    system_prompt = build_system_prompt(persona, user_id)

    if mode == "analysis":
        # 【关键升级】：先问 AI 应该用哪个工具
        tool_selection_prompt = f"""
        你是一个工具调度员。请根据用户问题，从以下工具列表中选择一个最合适的工具：
        - player_overview: 获取玩家整体概况 (总人数、平均时长等)
        - character_analysis: 分析角色受欢迎程度/分布
        - activity_analysis: 分析玩家活跃度等级
        - payment_analysis: 分析付费情况和营收
        - top_player: 寻找游戏时长最高的玩家
        
        用户问题: {question}
        
        请直接返回工具名称，不要输出其他文字。如果不需要工具，请返回 'none'。
        """
        
        try:
            # 调用一次轻量级请求来决定工具
            tool_choice = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{'role': 'user', 'content': tool_selection_prompt}]
            ).choices[0].message.content.strip()

            if tool_choice != 'none' and tool_choice in ["player_overview", "character_analysis", "activity_analysis", "payment_analysis", "top_player"]:
                # 调用实际的工具获取数据
                analysis_result = run_analysis_tool(tool_choice, {"question": question})
                user_content = f"【分析工具 {tool_choice} 返回的数据】：{analysis_result}\n\n【用户问题】：{question}"
            else:
                user_content = question
        except Exception as e:
            print(f"工具调度失败: {e}")
            user_content = question
    else:
        user_content = question

    # ... 剩下的调用云端 AI 的逻辑保持不变 ...

    # 3. 调用云端大模型 (OpenAI 格式)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_content},
            ],
            temperature=0.7
        )
        answer = response.choices[0].message.content
        
        # 4. 自动存入随笔记忆
        memory_mgr.add_memory(f"用户问: {question} | AI答: {answer[:30]}...")
        
    except Exception as e:
        print(f"API 调用失败: {e}")
        answer = "抱歉，我的云端大脑暂时断线了。"

    return answer

def run_analysis_tool(tool_name, params):
    """
    保留你原有的工具执行函数
    """
    return get_tool_result(tool_name, params)