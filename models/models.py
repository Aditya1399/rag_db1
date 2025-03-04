#necessary imports 
from sqlalchemy import create_engine, Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext
from datetime import datetime, timezone
from pydantic import BaseModel

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Document model
class Document(Base):
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

#Embedding model
class Embedding(Base):
    __tablename__ = "embeddings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(Integer)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))

#User model
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

#IngestRequest model    
class IngestRequest(BaseModel):
    title: str
    content: str

#QARequest Model Structure
class QARequest(BaseModel):
    question: str
    top_k: int 

#QAResponse Model Structure
class QAResponse(BaseModel):
    answer: str
    relevant_documents: list 

#Function to initialise the db given 
def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
