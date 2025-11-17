from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class Project(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    category: str = Field(..., description="Type of work: Ad, Music Video, Product, Model Shoot, etc.")
    thumbnail_url: str = Field(..., description="Thumbnail image URL for the project")
    video_url: Optional[str] = Field(None, description="Optional video URL or embed link")
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None


class ContactMessage(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    company: Optional[str] = None
    message: str = Field(..., min_length=10, max_length=2000)
    budget: Optional[str] = Field(None, description="Optional budget range text")
    service: Optional[str] = Field(None, description="Service of interest")


class ProjectOut(Project):
    id: Optional[str] = None
    created_at: Optional[datetime] = None


class ContactMessageOut(ContactMessage):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
