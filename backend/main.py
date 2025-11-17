from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from schemas import Project, ProjectOut, ContactMessage, ContactMessageOut
from database import db, create_document, get_documents

app = FastAPI(title="NFX Creations API", version="1.0.0")

# CORS - allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"]) 
async def root():
    return {"status": "ok", "service": "NFX Creations API"}


@app.get("/test", tags=["health"]) 
async def test_db():
    # Simple test to ensure database connectivity
    try:
        await db.command("ping")
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# Projects Endpoints
@app.post("/projects", response_model=ProjectOut, tags=["projects"])
async def create_project(project: Project):
    data = project.dict()
    doc = await create_document("project", data)
    return ProjectOut(**doc)


@app.get("/projects", response_model=List[ProjectOut], tags=["projects"])
async def list_projects(category: Optional[str] = None, limit: int = 24):
    filter_dict = {"category": category} if category else {}
    docs = await get_documents("project", filter_dict, limit)
    return [ProjectOut(**d) for d in docs]


# Contact Endpoints
@app.post("/contact", response_model=ContactMessageOut, tags=["contact"])
async def submit_contact(message: ContactMessage):
    data = message.dict()
    doc = await create_document("contactmessage", data)
    return ContactMessageOut(**doc)
