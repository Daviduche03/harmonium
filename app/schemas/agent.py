from typing import List
from pydantic import BaseModel


class AgentCreate(BaseModel):
    name: str
    role: str
    goal: str
    backstory: str

class TeamCreate(BaseModel):
    name: str
    agent_ids: List[int]

class TaskCreate(BaseModel):
    description: str
    agent_id: int
    expected_output: str