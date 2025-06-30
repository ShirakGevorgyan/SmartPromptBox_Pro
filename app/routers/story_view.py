from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_all_stories():
    return {"message": "Բոլոր պատմությունները այստեղ կլինեն"}

@router.get("/{story_id}")
def get_story_by_id(story_id: str):
    return {"message": f"Սա պատմությունն է՝ {story_id}"}
