import csv
import json

def transform_csv_to_profile(csv_path, json_path):
    profiles = {}
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p_id = row['player_id']
            # 将数值转化为描述性语言，这样 AI 更容易理解
            paid_level = "高付费" if float(row['paid']) > 0.8 else "普通玩家"
            
            profiles[p_id] = {
                "基本信息": f"年龄 {row['age']} 岁，来自 {row['region']}",
                "核心角色": row['character'],
                "游戏状态": f"累计游戏 {row['hours_played']} 小时，活跃度 {row['days_played']} 天",
                "消费标签": paid_level,
                "进度": f"等级完成度 {row['level_completion']}"
            }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    print(f"成功转换！画像已保存至 {json_path}")

# 执行转换
transform_csv_to_profile('data/players.csv', 'data/players.json')