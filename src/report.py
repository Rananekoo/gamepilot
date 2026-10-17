def generate_report(players):
    print("\n========== GamePilot 完整分析报告 ==========")

    # 1. 基础数据
    total_players = len(players)

    total_hours = 0
    total_days = 0
    active_players = 0

    for row in players:
        total_hours += int(row['hours_played'])
        total_days += int(row['days_played'])

        if int(row['days_played']) >= 7:
            active_players += 1

    avg_hours = total_hours / total_players
    avg_days = total_days / total_players

    print("\n【一、玩家概况】")
    print("玩家总数:", total_players)
    print("平均游戏时长:", round(avg_hours, 2), "小时")
    print("平均游戏天数:", round(avg_days, 2), "天")
    print("活跃玩家数:", active_players)

    # 2. 角色分析
    character_counts = {}

    for row in players:
        character = row['character']

        if character in character_counts:
            character_counts[character] += 1
        else:
            character_counts[character] = 1

    popular_character = max(
        character_counts,
        key=character_counts.get
    )

    print("\n【二、角色分析】")
    print("最受欢迎角色:", popular_character)
    print("使用人数:", character_counts[popular_character])

    # 3. 活跃度分析
    activity_counts = {
        "低活跃": 0,
        "中活跃": 0,
        "高活跃": 0
    }

    for row in players:
        days = int(row['days_played'])

        if days < 7:
            activity_counts["低活跃"] += 1
        elif days < 20:
            activity_counts["中活跃"] += 1
        else:
            activity_counts["高活跃"] += 1

    print("\n【三、游戏行为分析】")

    for level, count in activity_counts.items():
        print(level + ":", count, "人")

    # 4. 付费分析
    paying_players = 0
    total_revenue = 0

    for row in players:
        if int(row['paid']) == 1:
            paying_players += 1
            total_revenue += float(row['amount'])

    payment_rate = paying_players / total_players * 100

    arppu = (
        total_revenue / paying_players
        if paying_players > 0
        else 0
    )

    print("\n【四、付费分析】")
    print("付费玩家数:", paying_players)
    print("总收入:", round(total_revenue, 2))
    print("付费率:", round(payment_rate, 2), "%")
    print("ARPPU:", round(arppu, 2))

    print("\n========== 报告生成完成 ==========")