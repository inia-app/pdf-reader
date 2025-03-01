from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from handlers.ocr import read, read_url

#inicializando classes
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
    

@app.post('/upload_file')
async def main(file: UploadFile):
    extension = file.filename.split(".")[-1]
    accepted_forms = {"pdf":read, "jpg":read, "png":read}
    if extension not in accepted_forms.keys():
        raise HTTPException(status_code=500, detail="Invalid File Input")
    file_ = await accepted_forms[extension](file.file)

    return JSONResponse(
        {"content": file_}
    )
@app.post('/send-url')
async def main(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        extension = os.path.splitext(url)[-1][1:].lower()
        accepted_forms = {"pdf":read_url, "jpg":read_url, "png":read_url}
        if extension not in accepted_forms.keys():
            raise HTTPException(status_code=400, detail="Invalid File Input")
        file_ = await accepted_forms[extension](url)

        return JSONResponse(
            {"content": file_}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
# if __name__ == '__main__':
#     uvicorn.run("app:app", reload=True)