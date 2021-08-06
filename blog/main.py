from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import schemas, models 
from .database import Base, SessionLocal, engine


app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
	db = SessionLocal()

	try:
		yield db  
	finally:
		db.close()

@app.get('/articles')
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles


@app.post('/articles')
def create_article(request: schemas.Article, db: Session = Depends(get_db)):
    new_article = models.Article(title=request.title, body=request.body)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


