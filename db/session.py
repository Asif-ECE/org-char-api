from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

DATABASE_URL = "sqlite+aiosqlite:///./db/db.sqlite3"
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Set SQLite PRAGMA settings for the database connection.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

# Create a session factory for async sessions
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def initialize_db():
    """
    Initialize the database by creating all tables.
    Keeping this function here for future use.
    Currently, we are using Alembic for migrations.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """
    Get a new async session for the database.
    """
    async with async_session_factory() as session:
        yield session