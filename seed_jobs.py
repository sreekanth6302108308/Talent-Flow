import asyncio
from app.core.database import SessionLocal, engine
from app.models.job import Job
from app.models.user import User, UserRole
from sqlalchemy import select
from datetime import datetime

async def seed_job():
    async with SessionLocal() as db:
        # First check if there is a recruiter
        result = await db.execute(select(User).filter(User.role == UserRole.RECRUITER))
        recruiter = result.scalars().first()
        
        if not recruiter:
            print("No recruiter found. Creating one...")
            recruiter = User(
                email="recruiter@example.com",
                password="password",  # Plain text as per request
                full_name="Demo Recruiter",
                role=UserRole.RECRUITER,
                company_name="Tech Corp",
                company_description="A leading tech company."
            )
            db.add(recruiter)
            await db.commit()
            await db.refresh(recruiter)
            print(f"Created recruiter: {recruiter.email}")

        # Check if jobs exist
        result = await db.execute(select(Job))
        jobs = result.scalars().all()
        
        if not jobs:
            print("Seeding test job...")
            job = Job(
                title="Full Stack Developer",
                description="<p>We are looking for a skilled Full Stack Developer with React and Python experience.</p>",
                location="Remote",
                category="Engineering",
                salary_range="20k - 40k",
                job_image_url="",
                recruiter_id=recruiter.id,
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(job)
            await db.commit()
            print("Test job created successfully!")
        else:
            print(f"Jobs already exist: {len(jobs)}")

if __name__ == "__main__":
    asyncio.run(seed_job())
