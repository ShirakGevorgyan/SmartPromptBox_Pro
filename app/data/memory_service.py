from typing import List, Dict
from sqlalchemy.orm import Session
from app.data.models.memory_model import UserMemory

# 🧠 Բեռնել պատմությունը ըստ օգտատիրոջ
def load_history(session: Session, user_id: str) -> List[Dict[str, str]]:
    messages = (
        session.query(UserMemory)
        .filter_by(user_id=user_id)
        .order_by(UserMemory.id.asc())
        .all()
    )
    return [{"role": msg.role, "content": msg.content} for msg in messages]

# 💾 Պահել ամբողջ պատմությունը (մաքրել հինը՝ ավելացնել նորը)
def save_history(session: Session, user_id: str, history: List[Dict[str, str]]):
    # Ջնջում ենք հինը
    session.query(UserMemory).filter_by(user_id=user_id).delete()
    session.commit()

    # Ավելացնում ենք նորը
    for item in history:
        msg = UserMemory(
            user_id=user_id,
            role=item["role"],
            content=item["content"]
        )
        session.add(msg)
    session.commit()
