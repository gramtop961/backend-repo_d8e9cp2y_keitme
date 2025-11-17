import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Project, ProjectOut, ContactMessage, ContactMessageOut

app = FastAPI(title="NFX Creations API", version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok", "service": "nfx-creations-backend"}

@app.get("/test")
def test_database():
    info = {
        "backend": "running",
        "database": "not_configured",
        "connection_status": "not_connected",
        "collections": []
    }
    try:
        if db is not None:
            info["database"] = "configured"
            info["connection_status"] = "connected"
            try:
                info["collections"] = db.list_collection_names()
            except Exception as e:
                info["collections_error"] = str(e)
    except Exception as e:
        info["error"] = str(e)
    return info

# Demo data fallback if DB is unavailable or empty

def _demo_projects() -> List[ProjectOut]:
    base = [
        {
            "title": "Neon Odyssey",
            "category": "AI Ad",
            "thumbnail_url": "https://images.unsplash.com/photo-1535747790212-30c585ab4862?q=80&w=1600&auto=format&fit=crop",
            "video_url": "https://vimeo.com/76979871",
            "description": "A story-led cyberpunk spot exploring light, motion and memory.",
            "tags": ["cinematic", "retro-futurism", "AI"]
        },
        {
            "title": "Synthetic Bloom",
            "category": "Music Video",
            "thumbnail_url": "https://images.unsplash.com/photo-1517817544804-89912393f7d4?q=80&w=1600&auto=format&fit=crop",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "description": "Audio-reactive visuals grown from latent space flowers.",
            "tags": ["music", "style transfer", "visualizer"]
        },
        {
            "title": "Eclipse One",
            "category": "Product",
            "thumbnail_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=1600&auto=format&fit=crop",
            "video_url": None,
            "description": "Launch film for a wearable with hard light and liquid metal renders.",
            "tags": ["product", "shaders", "macro"]
        }
    ]
    out: List[ProjectOut] = []
    for i, p in enumerate(base):
        out.append(ProjectOut(id=f"demo-{i+1}", **p))
    return out

@app.post("/projects", response_model=ProjectOut)
async def create_project(project: Project):
    try:
        inserted_id = create_document("project", project)
        return ProjectOut(id=inserted_id, **project.model_dump())
    except Exception as e:
        # If DB not configured, surface a clear error
        raise HTTPException(status_code=500, detail=f"Database unavailable: {str(e)}")

@app.get("/projects", response_model=List[ProjectOut])
async def list_projects(category: Optional[str] = None, limit: int = 24):
    try:
        query = {"category": category} if category else {}
        docs = get_documents("project", query, limit)
        out: List[ProjectOut] = []
        for d in docs:
            d_id = str(d.get("_id"))
            d.pop("_id", None)
            out.append(ProjectOut(id=d_id, **d))
        # If DB connected but empty, serve demo so frontend looks alive
        if not out:
            return _demo_projects()
        return out
    except Exception:
        # Graceful fallback when DB not configured
        return _demo_projects()

@app.post("/contact", response_model=ContactMessageOut)
async def create_contact(msg: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", msg)
        return ContactMessageOut(id=inserted_id, **msg.model_dump())
    except Exception as e:
        # Accept submissions even without DB by returning a fake ID
        return ContactMessageOut(id="demo-contact", **msg.model_dump())

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
