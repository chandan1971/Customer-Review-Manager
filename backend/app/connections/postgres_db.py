from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from sqlalchemy.pool import NullPool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,     
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()  
    except:
        db.rollback()  
        raise
    finally:
        db.close()   
