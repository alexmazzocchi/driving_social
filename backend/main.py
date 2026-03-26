from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
import os

# ------------------------
# Setup DB + Models (minimo)
# ------------------------
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://drivingsocial:weakpassword@db:5432/drivingsocial")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    start_lat = Column(String(50))
    start_lng = Column(String(50))
    end_lat = Column(String(50))
    end_lng = Column(String(50))
    created_at = Column(DateTime, default=func.now())


Base.metadata.create_all(bind=engine)

# ------------------------
# API
# ------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/routes")
def create_route(
    title: str,
    description: str,
    start_lat: float,
    start_lng: float,
    end_lat: float,
    end_lng: float,
):
    db = SessionLocal()
    route = Route(
        title=title,
        description=description,
        start_lat=str(start_lat),
        start_lng=str(start_lng),
        end_lat=str(end_lat),
        end_lng=str(end_lng),
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    db.close()

    return {
        "id": route.id,
        "title": route.title,
        "description": route.description,
        "start": {"lat": route.start_lat, "lng": route.start_lng},
        "end": {"lat": route.end_lat, "lng": route.end_lng},
    }


@app.get("/routes")
def list_routes():
    db = SessionLocal()
    routes = db.query(Route).all()
    db.close()

    return [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "start": {"lat": r.start_lat, "lng": r.start_lng},
            "end": {"lat": r.end_lat, "lng": r.end_lng},
        }
        for r in routes
    ]


# ------------------------
# Upload foto
# ------------------------

STATICS_DIR = os.getenv("STATIC_DIR", "/static")
os.makedirs(STATICS_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(image: UploadFile = File(...)):
    file_path = os.path.join(STATICS_DIR, image.filename)
    with open(file_path, "wb") as f:
        f.write(await image.read())
    return {"filename": image.filename, "url": f"/static/images/{image.filename}"}


@app.get("/static/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join(STATICS_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse({"error": "file not found"}, status_code=404)
    return FileResponse(file_path)
