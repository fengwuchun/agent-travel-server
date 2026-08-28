
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agent.state import State
from agent.tools import calculator

# 加载环境变量 .env
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "qwen-turbo"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_API_BASE"),
)






