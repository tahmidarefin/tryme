from fastapi import FastAPI, File, UploadFile, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import QuestionCreate, ExamCreate, TokenCreate, UserCreate
from app.db import Question, Examination, create_db_and_table, get_async_session
from app.auth import authenticate_user, create_access_token, get_current_active_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import os
import uuid
import aiofiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

origins = ["*"]

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, # Specify allowed origins
    allow_credentials=True, # Allow cookies and credentials
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post('/upload')
async def upload(
    file: UploadFile = File(...)
):
    try:
        data = await file.read()
        filepath = os.path.join('./static/img', file.filename)
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(data)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong!')
    finally:
        await file.close()

    return {"message": "File uploaded successfully."}

# @app.get('/posts')
# def get_all_posts(limit: int = None):
#     if limit is not None:
#         limit = min(limit, len(text_posts))
#     return list(text_posts.values())[:limit]

# @app.get('/posts/{id}')
# def get_post(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found.")
#     return text_posts.get(id)

# @app.post('/posts')
# def create_post(post: PostCreate) -> PostCreate:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[len(text_posts.keys()) + 1] = new_post
#     return post

@app.post('/questions')
async def create_question(questions: list[QuestionCreate], session: AsyncSession = Depends(get_async_session)):
    for value in questions:
        question = Question(
            **value
            # title=value.title, 
            # complexity=value.complexity,
            # type=value.type,
            # options=value.options,
            # correct_answers=value.correct_answers,
            # max_score=value.max_score
        )
        session.add(question)
        await session.commit()
    
    return {"message": "Questions saved successfully."}

@app.get('/questions')
async def get_questions(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Question)) # return queryset for each query, not specific item
    questions = [row[0] for row in result.all()] # row[0] means first elements of queryset
    questions_data = [{
        "id": str(question.id),
        "title": question.title,
        "complexity": question.complexity,
        "type": question.type,
        "options": question.options,
        "correct_answers": question.correct_answers,
        "max_score": question.max_score
    } for question in questions]

    return {"questions": questions_data}

@app.delete('/questions/{question_id}')
async def delete_question(
    question_id: str, 
    session: AsyncSession = Depends(get_async_session)
):
    id = uuid.UUID(question_id)
    result = await session.execute(select(Question).where(Question.id == id))
    question = result.scalars().first()

    try:
        await session.delete(question)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Question was deleted successfully."}

@app.post('/exams')
async def create_exam(exam: ExamCreate, session: AsyncSession = Depends(get_async_session)):
    examination = Examination(
        **exam
        # title=exam.title, 
        # duration=exam.duration,
        # ques_list=exam.ques_list
    )
    session.add(examination)
    await session.commit()
    return {"message": "Examination saved successfully."}

@app.get('/exams')
async def get_exams(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Examination)) # return queryset for each query, not specific item
    exams = [row[0] for row in result.all()] # row[0] means first elements of queryset

    exams_data = []
    for exam in exams:
        ques_list = []
        for ques_id in exam.ques_list:
            id = uuid.UUID(ques_id)
            result = await session.execute(select(Question).where(Question.id == id))
            question = result.scalars().first()
            questions_data = {
                "id": str(question.id),
                "title": question.title,
                "complexity": question.complexity,
                "type": question.type,
                "options": question.options,
                "correct_answers": question.correct_answers,
                "max_score": question.max_score
            }
            ques_list.append(questions_data)
            
        exam_dict = {
            "id": str(exam.id), 
            "title": exam.title, 
            "duration": exam.duration, 
            "ques_list": ques_list
        }

        exams_data.append(exam_dict)
    return {"examinations": exams_data}

@app.post("/auth/token", response_model=TokenCreate)
async def login_for_access_token(form_data = Depends(OAuth2PasswordRequestForm), session: AsyncSession = Depends(get_async_session)):
  user = await authenticate_user(form_data.email, form_data.password)
  if user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  
  access_token = create_access_token(
      data={"sub": user.email}
  )

  return {"access_token": access_token, "token_type": "bearer"}

@app.get('/user', response_mode=UserCreate)
async def read_current_user(current_user: UserCreate = Depends(get_current_active_user)):
    return current_user