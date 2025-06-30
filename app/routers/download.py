from fastapi import APIRouter

router = APIRouter()

@router.get("/csv")
def download_csv():
    return {"message": "CSV ֆայլը կվերադարձվի այստեղ"}

@router.get("/pdf")
def download_pdf():
    return {"message": "PDF ֆայլը կվերադարձվի այստեղ"}

