import json
import ollama

from src.data_loader import load_data
from src.tools import (
    get_player_overview,
    get_character_analysis,
    get_activity_analysis,
    get_payment_analysis,
    get_top_player
)


players = load_data("data/players.csv")


def player_overview():
    return get_player_overview(players)


def character_analysis():
    return get_character_analysis(players)


def activity_analysis():
    return get_activity_analysis(players)


def payment_analysis():
    return get_payment_analysis(players)


def top_player():
    return get_top_player(players)


available_functions = {
    "player_overview": player_overview,
    "character_analysis": character_analysis,
    "activity_analysis": activity_analysis,
    "payment_analysis": payment_analysis,
    "top_player": top_player
}


tools = [
    player_overview,
    character_analysis,
    activity_analysis,
    payment_analysis,
    top_player
]


def generate_report():

    messages = [
        {
            "role": "system",
            "content": """
你是 GamePilot 的游戏数据分析专家。

请根据工具提供的真实数据，生成一份游戏运营分析报告。

报告必须包含：

1. 玩家整体情况
2. 角色情况
3. 玩家活跃度
4. 玩家付费情况
5. 关键发现
6. 游戏运营建议

要求：

- 所有数字必须来自工具返回的数据
- 不允许编造数据
- 分析要结合多个数据维度
- 运营建议必须有数据依据
- 使用中文
- 使用清晰的 Markdown 格式
- 不要过度重复原始数据
"""
        },
        {
            "role": "user",
            "content": """
请分析当前 GamePilot 的全部玩家数据，
主动调用你需要的工具，
最后生成一份完整的游戏运营分析报告。
"""
        }
    ]

    while True:

        response = ollama.chat(
            model="qwen3.5:9b",
            messages=messages,
            tools=tools
        )

        messages.append(response.message)

        # 如果模型已经完成分析
        if not response.message.tool_calls:
            return response.message.content

        # 执行模型要求调用的工具
        for tool_call in response.message.tool_calls:

            function_name = tool_call.function.name
            function_args = tool_call.function.arguments

            print(f"[调用工具] {function_name}")

            function_to_call = available_functions.get(function_name)

            if function_to_call is None:
                result = {
                    "error": f"找不到工具：{function_name}"
                }
            else:
                result = function_to_call(**function_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_name": function_name,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )


if __name__ == "__main__":

    print("================================")
    print("     GamePilot AI Analysis")
    print("================================")

    print("\n正在分析游戏数据，请稍等...\n")

    report = generate_report()

    print("\n")
    print(report)

    with open(
        "gamepilot_report.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)
    print("\n分析报告已保存为 gamepilot_report.md")