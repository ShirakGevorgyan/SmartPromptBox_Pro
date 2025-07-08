import os
from aiogram import Router
from aiogram.types import Message, InputFile

# 📂 PDF-երի ժամանակավոր պահոց
PDF_DIR = "app/temp"

router = Router()

# 🔍 Վերցնում ենք վերջին PDF ֆայլը ըստ ստեղծման ժամանակի
def get_last_pdf_file():
    if not os.path.exists(PDF_DIR):
        return None
    pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    if not pdfs:
        return None
    pdfs.sort(key=lambda f: os.path.getmtime(os.path.join(PDF_DIR, f)), reverse=True)
    return os.path.join(PDF_DIR, pdfs[0])

# ✅ PDF ուղարկող ռաութեր
@router.message(lambda message: message.text == "/send_last_pdf")
async def send_last_pdf(message: Message):
    pdf_path = get_last_pdf_file()
    if pdf_path:
        await message.answer_document(InputFile(pdf_path), caption="📄 Ահա վերջին PDF ֆայլը։")
    else:
        await message.answer("❌ Չկան ստեղծված PDF ֆայլեր։")
