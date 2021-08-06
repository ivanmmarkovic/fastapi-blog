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

@app.post('/articles')
def create_article(request: schemas.Article, db: Session = Depends(get_db)):
    new_article = models.Article(title=request.title, body=request.body)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.get('/articles')
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles

@app.get('/articles/{id}')
def get_articles(id:int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    return article

@app.put('/articles/{id}')
def put_article(id:int, request: schemas.Article, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id)
    article.update(request.dict(), synchronize_session=False)
    db.commit()
    return article.first()

@app.delete('/articles/{id}')
def destroy(id, db: Session = Depends(get_db)):
	article = db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
	db.commit()
	return {'deleted': True}



