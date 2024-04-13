from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.models import Bot
from pydantic import BaseModel
from Agent.langchain_agent import invoke_agent


def generate_unique_id():
    import uuid
    return str(uuid.uuid4())


class Item(BaseModel):
    name: str
    description: str | None = None
    web_search: bool
    unique_id: str
    instruction: str


class InvokeBot(BaseModel):
    input: str
    unique_id: str


router = APIRouter()


@router.get("/bots")
def get_bots(db: Session = Depends(get_db)):
    bots = db.query(Bot).all()
    return {"bots": bots}


@router.get("/bots/{bot_id}")
def get_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    return {"bot": bot}


@router.post("/bots")
def create_bot(item: Item, db: Session = Depends(get_db)):
    try:
        unique_id = generate_unique_id()
        bot_data = item.dict()
        bot_data["unique_id"] = unique_id
        db_bot = Bot(**bot_data)
        db.add(db_bot)
        db.commit()
        db.refresh(db_bot)
        return {"bot": db_bot}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bots/invoke")
def invoke_bot(item: InvokeBot, db: Session = Depends(get_db)):
    try:
        bot = db.query(Bot).filter(Bot.unique_id == item.unique_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        res = invoke_agent(bot, item.input)
        return {"bot": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
