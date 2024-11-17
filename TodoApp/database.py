from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_UL = "sqlite:///./todosapp.db"
POSTGRES_DATABASE_UL = "postgresql://jade:FZ0AuD7buU2qSpekpDKs7OCySIReKs9N@todoapplicationdatabase_x1sk/TodoApplicationDatabase"


engine = create_engine(POSTGRES_DATABASE_UL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
