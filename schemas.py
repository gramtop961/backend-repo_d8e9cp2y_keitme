from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# NFX Creations data models

class Project(BaseModel):
    title: str = Field(..., description="Project title")
    category: str = Field(..., description="Category such as AI Ad, Music Video, Product, Model Shoot, Visuals")
    thumbnail_url: str = Field(..., description="Thumbnail image URL")
    video_url: Optional[str] = Field(None, description="Optional video URL (YouTube/Vimeo/direct)")
    description: str = Field(..., description="Short description of the project")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering/search")

class ProjectOut(Project):
    id: str = Field(..., description="Document ID")

class ContactMessage(BaseModel):
    name: str = Field(...)
    email: EmailStr
    company: Optional[str] = None
    message: str = Field(..., min_length=5)
    budget: Optional[str] = None
    service: Optional[str] = Field(None, description="Requested service type")

class ContactMessageOut(ContactMessage):
    id: str = Field(...)
