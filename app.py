import os
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from run import _main
from variables import CFG_FOLDER, OUTPUT_FOLDER, STATIC_FOLDER

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    """Serve the main HTML page."""
    index_path = os.path.join(STATIC_FOLDER, "index.html")
    if not os.path.isfile(index_path):
        raise HTTPException(status_code=500, detail="Index HTML not found")
    with open(index_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/api/configs")
async def list_configs() -> JSONResponse:
    """Return a list of available JSON config files."""
    if not os.path.isdir(CFG_FOLDER):
        raise HTTPException(status_code=500, detail=f"Config folder not found: {CFG_FOLDER}")
    files = [f for f in os.listdir(CFG_FOLDER) if f.endswith(".json")]
    return JSONResponse(content=files)


def convert_to_pdf(input_path: str) -> str:
    """Convert a DOCX file to PDF using pandoc."""
    if not input_path.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Input file is not a DOCX")
    output_path = os.path.splitext(input_path)[0] + ".pdf"
    try:
        subprocess.run(["pandoc", input_path, "-o", output_path], check=True)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Pandoc not found. Please install pandoc.")
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Pandoc conversion failed: {e}")
    return output_path


@app.get("/api/generate")
async def generate(config: str, format: str = "docx") -> JSONResponse:
    """Generate test and answer files and return download URLs."""
    if config not in os.listdir(CFG_FOLDER):
        raise HTTPException(status_code=400, detail="Invalid config file selected")
    test_docx, ans_docx = _main(config)
    if format == "pdf":
        test_file = convert_to_pdf(test_docx)
        ans_file = convert_to_pdf(ans_docx)
    else:
        test_file = test_docx
        ans_file = ans_docx

    test_name = os.path.basename(test_file)
    ans_name = os.path.basename(ans_file)
    return JSONResponse(content={
        "test": {"filename": test_name, "url": f"/download/{test_name}"},
        "ans": {"filename": ans_name, "url": f"/download/{ans_name}"},
    })


@app.get("/download/{filename}")
async def download_file(filename: str) -> FileResponse:
    """Serve a generated file from the output directory."""
    safe_name = os.path.basename(filename)
    file_path = os.path.join(OUTPUT_FOLDER, safe_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=safe_name)