import pdfplumber

with pdfplumber.open("./test2.pdf") as pdf:
    first_page = pdf.pages[13]
    print(first_page.extract_text())
