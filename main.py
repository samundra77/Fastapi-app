from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./count.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Counter(Base):
    __tablename__ = "counters"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# FastAPI route
@app.get("/count")
def read_count():
    db = SessionLocal()
    counter = db.query(Counter).first()
    if not counter:
        counter = Counter(count=0)
        db.add(counter)
        db.commit()
    counter.count += 1
    db.commit()
    return {"count": counter.count}

