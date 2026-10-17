from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent import ask_agent
from src.memory import MemoryManager

# 【关键修复】：创建 MemoryManager 实例，这样下面的接口才能调用它
memory_mgr = MemoryManager()

app = FastAPI(
    title="GamePilot API",
    description="GamePilot AI Game Data Analysis Agent",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有来源访问 (开发环境下最方便)
    allow_credentials=True,
    allow_methods=["*"], # 允许所有请求方法 (GET, POST, DELETE 等)
    allow_headers=["*"], # 允许所有请求头
)
# ==============================
# 请求数据格式
# ==============================

class Question(BaseModel):
    question: str
    persona: str = ""
    mode: str = "analysis"

class MemoryItem(BaseModel):
    content: str

# ==============================
# 基础接口
# ==============================

@app.get("/")
def home():
    return {
        "message": "GamePilot API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# ==============================
# AI聊天接口
# ==============================

@app.post("/chat")
def chat(data: Question):
    answer = ask_agent(
        question=data.question,
        persona=data.persona,
        mode=data.mode
    )

    return {
        "status": "success",
        "question": data.question,
        "answer": answer,
        "mode": data.mode
    }

# ==============================
# 长期记忆接口
# ==============================

@app.get("/memory")
def get_all_memory():
    """
    获取所有长期记忆
    """
    return {
        "status": "success",  # 明确告诉前端请求成功了
   
        "memories": memory_mgr.load_memory()
    }

@app.post("/memory")
def create_memory(data: MemoryItem):
    """
    手动添加一条长期记忆
    """
    content = data.content.strip()

    if not content:
        return {
            "success": False,
            "message": "记忆内容不能为空"
        }

    # 【修复】：使用 memory_mgr 实例调用
    memory_mgr.add_memory(content)

    return {
        "success": True,
        "message": "记忆添加成功",
        "memories": memory_mgr.load_memory()
    }

@app.post("/memory/delete") # 改为 POST，并明确路径
def remove_memory(data: MemoryItem):
    content = data.content.strip()
    if not content:
        return {"success": False, "message": "内容不能为空"}

    # 让 delete_memory 返回一个 True/False，告诉我们到底删掉没
    success = memory_mgr.delete_memory(content) 

    return {
        "success": success, # 不要直接写 True，要根据结果返回
        "message": "删除成功" if success else "未找到匹配记忆",
        "memories": memory_mgr.load_memory()
    }

@app.post("/memory/clear")
def remove_all_memory():
    """
    清空所有长期记忆
    """
    # 【修复】：使用 memory_mgr 实例调用 (请确保 memory.py 中实现了 clear_memory 方法)
    if hasattr(memory_mgr, 'clear_memory'):
        memory_mgr.clear_memory()

    return {
        "success": True,
        "message": "所有记忆已经清空",
        "memories": []
    }