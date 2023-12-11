from database.models import EngineDB, Base

async def start_db():
    async with EngineDB.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
