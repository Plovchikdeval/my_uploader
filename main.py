from fastapi import FastAPI, HTTPException, Request
import httpx
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Эндпоинт для загрузки файла с URL на сервер
@app.post("/fetch/")
async def fetch_file(request: Request):
    url = request.query_params.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")

    try:
        # Скачиваем файл с помощью httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Если код состояния не 2xx, будет выброшено исключение
        
        # Генерируем имя файла из URL (последний сегмент после "/")
        file_name = os.path.basename(url)
        
        # Сохраняем файл в локальную директорию
        file_path = f"./downloads/{file_name}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(response.content)

        # Формируем полный URL для скачивания файла
        server_url = f"http://176.123.163.14:8000/files/{file_name}"

        return {
            "link": server_url  # Полный URL для скачивания
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Эндпоинт для отдачи скачанного файла по запросу
@app.get("/files/{file_name}")
async def get_file(file_name: str):
    file_path = f"./downloads/{file_name}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)
