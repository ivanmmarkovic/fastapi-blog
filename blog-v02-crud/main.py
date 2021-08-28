from typing import Optional

from fastapi import FastAPI, Depends, status, Response, HTTPException 

import schemas, models

from schemas import Article
from models import ArticleModel
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
def delete_article(id: int, article: Article, db: Session = Depends(get_db)):
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




