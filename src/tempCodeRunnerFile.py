from loaders import load_pdf, load_docx, load_txt

file_path = "/Users/ekaanshjain/Desktop/proof_resources_grant1.pdf"  # Replace with your uploaded file

if file_path.endswith(".pdf"):
    docs = load_pdf(file_path)
elif file_path.endswith(".docx"):
    docs = load_docx(file_path)
else:
    docs = load_txt(file_path)

print(f"Loaded {len(docs)} pages/chunks.")
print("First 500 characters of first page:\n")
print(docs[0].page_content[:500])