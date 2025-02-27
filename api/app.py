from markitdown import MarkItDown
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from handlers.ocr import read

#inicializando classes
app = FastAPI()

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy"}, status_code=200)
    

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
if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)