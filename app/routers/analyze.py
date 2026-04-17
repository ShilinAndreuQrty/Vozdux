from fastapi import APIRouter
from app.models import UserInput

router = APIRouter()

@router.post('/analyze')
def analyze(user_input: UserInput):
    return {
        "best" : None,
        "alternatives" : [],
        "explanation" : "Дмитрий Пономарёв лох"
    }