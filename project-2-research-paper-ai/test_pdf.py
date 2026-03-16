from app.pdf_loader import load_pdf

print("Attempting to load the PDF...")

docs = load_pdf("sample_paper.pdf")

# This is the part that shows you the results
print(f"Success! Number of pages found: {len(docs)}")

if len(docs) > 0:
    print("--- First 500 characters of Page 1 ---")
    print(docs[0].page_content[:500])
else:
    print("The PDF was loaded but seems to be empty.")