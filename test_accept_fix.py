import asyncio
import httpx
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Credentials (assuming these exist or we create them)
RECRUITER_EMAIL = "recruiter_fix_test@example.com"
PASSWORD = "password123"
SEEKER_EMAIL = "seeker_fix_test@example.com"

async def test_accept_flow():
    async with httpx.AsyncClient() as client:
        print("1. Setup Users...")
        # Create Recruiter
        r_signup = await client.post(f"{BASE_URL}/auth/signup", data={
            "full_name": "Test Recruiter", "email": RECRUITER_EMAIL, "password": PASSWORD, "role": "recruiter", "company_name": "TestCorp"
        })
        
        # Login Recruiter
        r_login = await client.post(f"{BASE_URL}/auth/login", data={"username": RECRUITER_EMAIL, "password": PASSWORD})
        if r_login.status_code != 200:
            print(f"Recruiter Login Failed: {r_login.text}")
            return
        r_token = r_login.json()["access_token"]
        r_headers = {"Authorization": f"Bearer {r_token}"}

        # Create Seeker
        s_signup = await client.post(f"{BASE_URL}/auth/signup", data={
            "full_name": "Test Seeker", "email": SEEKER_EMAIL, "password": PASSWORD, "role": "job_seeker"
        })
        
        # Login Seeker
        s_login = await client.post(f"{BASE_URL}/auth/login", data={"username": SEEKER_EMAIL, "password": PASSWORD})
        s_token = s_login.json()["access_token"]
        s_headers = {"Authorization": f"Bearer {s_token}"}

        print("2. Post Job...")
        job_res = await client.post(f"{BASE_URL}/jobs/", json={
            "title": "Status Test Job", "description": "Desc", "category": "Dev", "location": "Remote", "salary_range": "500"
        }, headers=r_headers)
        if job_res.status_code != 200:
             print(job_res.text)
        job_id = job_res.json()["id"]

        print(f"3. Apply for Job {job_id}...")
        app_res = await client.post(f"{BASE_URL}/applications/{job_id}/apply", headers=s_headers)
        if app_res.status_code != 200:
             if "already applied" in app_res.text:
                 pass # Acceptable if re-running
             else:
                 print(f"Apply failed: {app_res.text}")
                 return
        
        # We need application ID. Seeker can list their apps.
        my_apps = await client.get(f"{BASE_URL}/applications/me", headers=s_headers)
        app_id = my_apps.json()[0]["id"]
        print(f"   Application ID: {app_id}")

        print("4. Attempt to ACCEPT application...")
        accept_res = await client.put(f"{BASE_URL}/applications/{app_id}/status?status=accept", headers=r_headers)
        
        print(f"   Status Code: {accept_res.status_code}")
        print(f"   Response: {accept_res.text}")

        if accept_res.status_code == 200 and accept_res.json()["status"] == "accepted":
            print("SUCCESS: Application Accepted!")
        else:
            print("FAILURE: Could not accept.")

if __name__ == "__main__":
    asyncio.run(test_accept_flow())
