import asyncio
import sys
import os

# Ensure we can import from app
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

async def main():
    print(f"Connecting to database to update schema...")
    # Create engine directly
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        print("Attempting to add missing columns...")
        
        # Add mobile_number
        try:
            print("Adding mobile_number column...")
            await conn.execute(text("ALTER TABLE users ADD COLUMN mobile_number VARCHAR(20) NULL"))
            print("Successfully added mobile_number.")
        except Exception as e:
            # Error 1060 is "Duplicate column name"
            if "1060" in str(e):
                print("Column mobile_number already exists.")
            else:
                print(f"Error adding mobile_number: {e}")

        # Add profile_picture_url
        try:
            print("Adding profile_picture_url column...")
            await conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture_url VARCHAR(500) NULL"))
            print("Successfully added profile_picture_url.")
        except Exception as e:
            if "1060" in str(e):
                print("Column profile_picture_url already exists.")
            else:
                print(f"Error adding profile_picture_url: {e}")

    await engine.dispose()
    print("Schema update check complete.")

if __name__ == "__main__":
    asyncio.run(main())
