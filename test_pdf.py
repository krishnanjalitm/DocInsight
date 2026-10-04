from pdf_processor import extract_text_from_pdf

text = extract_text_from_pdf("uploads/Module_1_IOT_Part_1.pptx.pdf")

print(text[:2000])