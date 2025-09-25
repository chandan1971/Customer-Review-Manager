from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from sqlalchemy.pool import NullPool
import ssl


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,     
    pool_pre_ping=True,
    connect_args={"ssl_context": ssl_context}
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
