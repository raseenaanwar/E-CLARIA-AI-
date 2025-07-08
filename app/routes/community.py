from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.ai.qa_agent import classify_tags_llama, suggest_answer_llama
from fastapi import status


router = APIRouter(prefix="/community", tags=["Community Q&A"])

@router.post("/question", response_model=schemas.QuestionOut)
def post_question(data: schemas.QuestionCreate, db: Session = Depends(get_db)):
    question = models.Question(**data.dict())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@router.post("/answer", response_model=schemas.AnswerOut)
def post_answer(data: schemas.AnswerCreate, db: Session = Depends(get_db)):
    answer = models.Answer(**data.dict())
    db.add(answer)
    db.commit()
    db.refresh(answer)

    # Bonus: Add points for answering
    user_points = db.query(models.Points).filter(models.Points.user_id == data.user_id).first()
    if not user_points:
        user_points = models.Points(user_id=data.user_id, score=5)
        db.add(user_points)
    else:
        user_points.score += 5
    db.commit()

    return answer

@router.get("/questions", response_model=list[schemas.QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()

@router.get("/answers/{question_id}", response_model=list[schemas.AnswerOut])
def list_answers(question_id: int, db: Session = Depends(get_db)):
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()

@router.get("/points/{user_id}", response_model=schemas.PointsOut)
def get_points(user_id: int, db: Session = Depends(get_db)):
    points = db.query(models.Points).filter(models.Points.user_id == user_id).first()
    if not points:
        raise HTTPException(status_code=404, detail="Points not found")
    return points


@router.post("/answer/{answer_id}/upvote")
def upvote_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer.upvotes = (answer.upvotes or 0) + 1
    db.commit()
    return {"message": "Answer upvoted"}


@router.get("/suggested_answer/{question_id}")
def get_suggested_answer(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    ai_answer = suggest_answer_llama(question.content)
    return {"suggested_answer": ai_answer}


@router.delete("/answer/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    db.delete(answer)
    db.commit()
    return