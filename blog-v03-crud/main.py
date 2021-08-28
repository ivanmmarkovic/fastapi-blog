from typing import Optional

from fastapi import FastAPI, Depends, status, Response, HTTPException 

import schemas, models

from schemas import Article, User
from models import ArticleModel, UserModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post('/articles', status_code=status.HTTP_201_CREATED)
def create_article(article: Article, db: Session = Depends(get_db)):
    article = ArticleModel(title=article.title, body=article.body)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@app.get('/articles', status_code=status.HTTP_200_OK)
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(ArticleModel).all()
    return articles

@app.get('/articles/{id}', status_code=status.HTTP_200_OK)
def get_article(id: int, response: Response, db: Session = Depends(get_db)):
    article = db.query(ArticleModel).filter(ArticleModel.id == id).first()
    if not article:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': f'Article with id {id} not found',
            'article': None
        }
    return article

@app.put('/articles/{id}')
def update_article(id: int, article: Article, db: Session = Depends(get_db)):
    articles = db.query(ArticleModel).filter(ArticleModel.id == id)
    if not articles.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f'Article with id {id} not found')
    articles.update(article.dict(), synchronize_session=False)
    db.commit()
    return article

@app.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(get_db)):
    articles = db.query(ArticleModel).filter(ArticleModel.id == id)
    if not articles.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f'Article with id {id} not found')
    articles.delete(synchronize_session=False)
    db.commit()
    return



####################################################################

@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: User, db: Session = Depends(get_db)):
    user = UserModel(name=user.name, email=user.email, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/users', status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@app.get('/users/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': f'User with id {id} not found',
            'user': None
        }
    return user

@app.put('/users/{id}')
def update_user(id: int, user: User, db: Session = Depends(get_db)):
    users = db.query(UserModel).filter(UserModel.id == id)
    if not users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f'Userwith id {id} not found')
    users.update(user.dict(), synchronize_session=False)
    db.commit()
    return user

@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    users = db.query(UserModel).filter(UserModel.id == id)
    if not users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f'User with id {id} not found')
    users.delete(synchronize_session=False)
    db.commit()
    return


