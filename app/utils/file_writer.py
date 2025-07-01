import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

TEMP_DIR = "app/temp"

def save_as_txt_and_pdf(lyrics: str, filename: str):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    # 📄 TXT ֆայլ
    txt_path = os.path.join(TEMP_DIR, f"{filename}.txt")
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(lyrics)

    # 📄 PDF ֆայլ
    pdf_path = os.path.join(TEMP_DIR, f"{filename}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 40
    for line in lyrics.split("\n"):
        c.drawString(40, y, line)
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()

    return txt_path, pdf_path
