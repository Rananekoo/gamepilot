from src.visualization import (show_activity_chart, show_payment_chart, show_character_chart)
from src.data_loader import load_data
from src.report import generate_report
players = load_data('data/players.csv')
#打印菜单标题
print("=== GamePilot ===")
print("==================")

#打印菜单选项
print("1. 查看数据概况")
print("2. 玩家分析")
print("3. 角色分析")
print("4. 游戏行为分析")
print("5. 付费分析")
print("6. 生成完整报告")
print("7. 生角色数据可视化")
print("8. 活跃度数据可视化")
print("9. 付费数据可视化")
print("0. 退出")

print()

#获取用户输入
while True:
    choice = input("请输入选项编号：")
    if choice not in ["1", "2", "3", "4", "5", "6","7","8","9","0"]:
        print("无效的选项，请重新输入")
        continue
    if choice == "1":
        print("您选择了查看数据概况")
        print("玩家总数:", len(players))
        total_hours = 0
        for row in players:
            total_hours += int(row['hours_played'])
        print("平均游戏时长:", total_hours / len(players))
        total_days = 0
        for row in players:
            total_days += int(row['days_played'])
        print("平均游戏天数:", total_days / len(players))
        active_players = 0
        for row in players:
            if int(row['days_played']) >= 7:
                active_players += 1
        print("活跃玩家数:", active_players)
    elif choice == "2":
        max_hours = 0
        top_player = ""
        for row in players:
            if int(row['hours_played']) > max_hours:
                max_hours = int(row['hours_played'])
                top_player = row['player_id']
        print(f"游戏时长最高玩家:{top_player},游戏时长:{max_hours}小时")
    elif choice == "3":
        character_counts = {}
        for row in players:
            character = row['character']
            if character in character_counts:
                character_counts[character] += 1
            else:
                character_counts[character] = 1
        for character, count in character_counts.items():
            print(f"角色:{character},数量:{count}人,占比:{count / len(players) * 100:.2f}%")
        print(f"最受欢迎的角色是:{max(character_counts, key=character_counts.get)},使用人数:{max(character_counts.values())}人")
    elif choice == "4":
            total_hours = 0
            for row in players:
                total_hours += int(row['hours_played'])
            print("平均游戏时长:", total_hours / len(players))
            total_days = 0
            for row in players:
                total_days += int(row['days_played'])
            print("平均游戏天数:", total_days / len(players))
            active_players = 0
            for row in players:
                if int(row['days_played']) >= 7:
                    active_players += 1
            print("活跃玩家数:", active_players)
            activity_counts = {}
            for row in players:
                if int(row['days_played']) < 7:
                    activity_level = "低活跃"
                elif int(row['days_played']) < 20:
                    activity_level = "中活跃"
                else:
                    activity_level = "高活跃"
                if activity_level in activity_counts:
                 activity_counts[activity_level] += 1
                else:
                    activity_counts[activity_level] = 1
            for activity_level, count in activity_counts.items():
                print(f"{activity_level}:{count}人")         
    elif choice == "5":
         paying_players = 0
         total_revenue = 0
         for row in players:
             if int(row['paid']) == 1:
                 paying_players += 1
                 total_revenue += float(row['amount'])
         print("付费玩家数:", paying_players)
         print("总收入:", total_revenue)
         print("付费率:", paying_players / len(players) * 100, "%")
         print("ARPPU:", total_revenue / paying_players if paying_players > 0 else 0)
    elif choice == "6":
         print("生成完整报告中...")
         generate_report(players)
         #生成报告的代码    
    elif choice == "7":
            print("生成角色数据可视化中...")
            show_character_chart(players)
            #生成角色数据可视化的代码
    elif choice == "8":
            print("生成活跃度数据可视化中...")
            show_activity_chart(players)
            #生成活跃度数据可视化的代码
    elif choice == "9":
            print("生成付费数据可视化中...")
            show_payment_chart(players)
            #生成付费数据可视化的代码
    elif choice == "0":
         print("已退出程序")
         exit()
    #根据用户输入执行相应操作
    
    