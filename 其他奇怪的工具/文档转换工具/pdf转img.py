import fitz

pdf_path = "『甘々と甘出し』台本（製品版）.pdf"
doc = fitz.open(pdf_path)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)   # 控制清晰度，默认72
    pix.save(f"page_{i+1}.png")