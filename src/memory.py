import json
import os

class MemoryManager:
    def __init__(self):
        # 档案路径 (CSV转换来的)
        self.profile_path = "data/players.json"
        # 随笔路径 (你原来写的 memory.json)
        self.memory_file = "memory.json" 

    # --- 维度 A：读取静态画像 (我建议的) ---
    def get_player_profile(self, user_id):
        try:
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
                user_data = profiles.get(str(user_id), {})
                if not user_data: return "暂无已知档案"
                return "\n".join([f"{k}: {v}" for k, v in user_data.items()])
        except Exception:
            return "暂无已知档案"

    # --- 维度 B：管理随笔记忆 (你原来写的) ---
    def load_memory(self):
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_memory(self, memory):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)

    def add_memory(self, content):
        memory = self.load_memory()
        memory.append(content)
        self.save_memory(memory)

    def delete_memory(self, content):
        memory = self.load_memory()
        # 只要记忆内容中包含了传入的字符串，就将其过滤掉
        # 这样可以避免因为空格、换行或微小差异导致删不掉
        new_memory = [m for m in memory if content.strip() not in m]
        
        if len(new_memory) != len(memory):
            self.save_memory(new_memory)
            return True
        return False