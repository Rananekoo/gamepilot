from src.data_loader import load_data  
# 工具调度员
def get_tool_result(tool_name, params=None):
    """
    调度员：根据 tool_name 调用对应的分析函数
    """
    # 1. 加载玩家数据
    players = load_data('data/players.csv') 
    
    # 2. 建立映射表：将 AI 识别的工具名 映射到 Python 函数
    tools_map = {
        "player_overview": get_player_overview,
        "character_analysis": get_character_analysis,
        "activity_analysis": get_activity_analysis,
        "payment_analysis": get_payment_analysis,
        "top_player": get_top_player,
    }
    
    # 3. 执行对应的函数并返回结果
    func = tools_map.get(tool_name)
    if func:
        return func(players)
    
    return {"error": f"未找到名为 {tool_name} 的分析工具"}

def get_player_overview(players):
    """获取玩家基本数据概况"""

    total_players = len(players)

    total_hours = 0
    total_days = 0
    active_players = 0

    for row in players:
        total_hours += int(row["hours_played"])
        total_days += int(row["days_played"])

        if int(row["days_played"]) >= 7:
            active_players += 1

    avg_hours = total_hours / total_players
    avg_days = total_days / total_players

    return {
        "total_players": total_players,
        "average_hours": round(avg_hours, 2),
        "average_days": round(avg_days, 2),
        "active_players": active_players
    }


def get_character_analysis(players):
    """分析角色使用情况"""

    character_counts = {}

    for row in players:
        character = row["character"]

        if character not in character_counts:
            character_counts[character] = 0

        character_counts[character] += 1

    popular_character = max(
        character_counts,
        key=character_counts.get
    )

    return {
        "character_counts": character_counts,
        "most_popular_character": popular_character,
        "most_popular_count": character_counts[popular_character]
    }


def get_activity_analysis(players):
    """分析玩家活跃程度"""

    activity_counts = {
        "低活跃": 0,
        "中活跃": 0,
        "高活跃": 0
    }

    for row in players:
        days = int(row["days_played"])

        if days < 7:
            activity_counts["低活跃"] += 1
        elif days < 20:
            activity_counts["中活跃"] += 1
        else:
            activity_counts["高活跃"] += 1

    return activity_counts


def get_payment_analysis(players):
    """分析玩家付费情况"""

    paying_players = 0
    total_revenue = 0

    for row in players:
        if int(row["paid"]) == 1:
            paying_players += 1
            total_revenue += float(row["amount"])

    total_players = len(players)

    payment_rate = paying_players / total_players * 100

    arppu = (
        total_revenue / paying_players
        if paying_players > 0
        else 0
    )

    return {
        "paying_players": paying_players,
        "total_revenue": round(total_revenue, 2),
        "payment_rate": round(payment_rate, 2),
        "arppu": round(arppu, 2)
    }


def get_top_player(players):
    """寻找游戏时长最高的玩家"""

    top_player = None
    max_hours = 0

    for row in players:
        hours = int(row["hours_played"])

        if hours > max_hours:
            max_hours = hours
            top_player = row["player_id"]

    return {
        "player_id": top_player,
        "hours_played": max_hours
    }