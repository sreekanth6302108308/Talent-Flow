import asyncio
from app.core.database import SessionLocal
from app.models.job import Job
from app.models.user import User, UserRole
from sqlalchemy import select
from datetime import datetime

# Data extracted from assets.js
jobs_data = [
    {
        "title": "Full Stack Developer",
        "location": "California",
        "level": "Senior Level",
        "company": "Microsoft",
        "description": "<p>We are seeking a highly skilled Full Stack Developer...</p>",
        "salary": "82k",
        "category": "Programming"
    },
    {
        "title": "Data Scientist",
        "location": "New York",
        "level": "Intermediate Level",
        "company": "Walmart",
        "description": "<p>Join our analytics team to help drive business decisions...</p>",
        "salary": "72k",
        "category": "Data Science"
    },
    {
        "title": "UI/UX Designer",
        "location": "Bangalore",
        "level": "Beginner Level",
        "company": "Accenture",
        "description": "<p>Create intuitive digital experiences as a UI/UX Designer...</p>",
        "salary": "61k",
        "category": "Designing"
    },
    {
        "title": "DevOps Engineer",
        "location": "Washington",
        "level": "Senior Level",
        "company": "Samsung",
        "description": "<p>Enhance our deployment pipeline as a DevOps Engineer...</p>",
        "salary": "53k",
        "category": "Programming"
    },
    {
        "title": "Software Engineer",
        "location": "Hyderabad",
        "level": "Intermediate Level",
        "company": "Amazon",
        "description": "<p>Join our team as a Software Engineer...</p>",
        "salary": "91k",
        "category": "Programming"
    },
    {
        "title": "Network Engineer",
        "location": "Bangalore",
        "level": "Senior Level",
        "company": "Adobe",
        "description": "<p>We are looking for a Network Engineer...</p>",
        "salary": "77k",
        "category": "Networking"
    },
    {
        "title": "Project Manager",
        "location": "Bangalore",
        "level": "Senior Level",
        "company": "Slack",
        "description": "<p>Lead projects as a Project Manager ensuring timely delivery...</p>",
        "salary": "60k",
        "category": "Management"
    }
]

async def seed_full_jobs():
    async with SessionLocal() as db:
        print("Starting seed process...")
        
        for job_data in jobs_data:
            company_name = job_data["company"]
            
            # 1. Find or Create Recruiter for this company
            result = await db.execute(select(User).filter(User.company_name == company_name))
            recruiter = result.scalars().first()
            
            if not recruiter:
                print(f"Creating recruiter for {company_name}...")
                recruiter = User(
                    email=f"recruiter_{company_name.lower()}@example.com",
                    password="password",
                    full_name=f"{company_name} Recruiter",
                    role=UserRole.RECRUITER,
                    company_name=company_name,
                    company_description=f"This is {company_name}."
                )
                db.add(recruiter)
                await db.commit()
                await db.refresh(recruiter)
            
            # 2. Check if job already exists (simple title + company check)
            result = await db.execute(
                select(Job).filter(Job.title == job_data["title"], Job.recruiter_id == recruiter.id)
            )
            existing_job = result.scalars().first()
            
            if not existing_job:
                print(f"Creating job: {job_data['title']} at {company_name}")
                new_job = Job(
                    title=job_data["title"],
                    description=job_data["description"],
                    location=job_data["location"],
                    category=job_data["category"],
                    salary_range=job_data["salary"],
                    job_image_url="", # Placeholder, frontend handles missing images
                    recruiter_id=recruiter.id,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(new_job)
            else:
                print(f"Job exists: {job_data['title']} at {company_name}")
        
        await db.commit()
        print("Seed completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_full_jobs())
