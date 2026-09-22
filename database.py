from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Adatbázis elérési útja (Connection URL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./webshop.db"

# 2. Az Engine létrehozása
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. Munkamenet-gyár (Session factory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Alaposztály a táblamodellekhez
Base = declarative_base()

# 5. Függőség (Dependency) a FastAPI végpontok számára
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()