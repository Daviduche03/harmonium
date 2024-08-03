# app/api/endpoints/bot.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.agent import AgentCreate, TeamCreate, TaskCreate
from app.models.agent import AgentModel
from app.models.team import TeamModel, TeamMember
from app.api import deps
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException

router = APIRouter()

@router.post("/")
def create_agent(
    agent: AgentCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_agent = AgentModel(**agent.model_dump(), user_id=current_user.id)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.post("/teams/create")
def create_team(team: TeamCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_team = TeamModel(name=team.name, user_id=current_user.id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    for agent_id in team.agent_ids:
        team_member = TeamMember(team_id=db_team.id, agent_id=agent_id)
        db.add(team_member)
    
    db.commit()
    return db_team

@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(deps.get_db)):
    agent = db.query(AgentModel).filter(AgentModel.id == task.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    crew_agent = Agent(
        role=agent.role,
        goal=agent.goal,
        backstory=agent.backstory,
        allow_delegation=False
    )

    crew_task = Task(
        description=task.description,
        agent=crew_agent,
        expected_output=task.expected_output
    )

    crew = Crew(
        agents=[crew_agent],
        tasks=[crew_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    return {"result": result}

@router.post("/run_team/")
def run_team(team_id: int, task_description: str, db: Session = Depends(deps.get_db)):
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    team_members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    agents = []
    for member in team_members:
        agent = db.query(AgentModel).filter(AgentModel.id == member.agent_id).first()
        crew_agent = Agent(
            role=agent.role,
            goal=agent.goal,
            backstory=agent.backstory,
            allow_delegation=True
        )
        agents.append(crew_agent)

    task = Task(
        description=task_description,
        agent=agents[0],  # Assign to the first agent, but allow delegation
    )

    crew = Crew(
        agents=agents,
        tasks=[task],
        process=Process.hierarchical  # Use hierarchical process for team collaboration
    )

    result = crew.kickoff()
    return {"result": result}