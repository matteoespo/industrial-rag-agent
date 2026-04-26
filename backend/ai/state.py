from typing import TypedDict, List

class AgentState(TypedDict):
    """Represents the state of an agent in the system."""
    query: str
    documents: List[str]
    answer: str
    chat_history: List[dict]  # [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi there!"}]
