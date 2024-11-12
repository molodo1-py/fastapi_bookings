import shutil

from fastapi import APIRouter, UploadFile, status

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Upload images"])


@router.post("/hotels", status_code=status.HTTP_201_CREATED)
async def add_hotel_image(name: int, file: UploadFile):
    img_path = f"app/static/images/{name}.webp"
    with open(img_path, "wb+") as f:
        shutil.copyfileobj(file.file, f)
    process_pic.delay(img_path)
