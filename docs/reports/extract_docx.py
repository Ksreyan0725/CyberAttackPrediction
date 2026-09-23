import zipfile
import os

docx_path = r"c:\Users\sreya\OneDrive\Desktop\Project\docs\project report format.docx"
extract_path = r"c:\Users\sreya\OneDrive\Desktop\Project\docs\extracted_format"

if not os.path.exists(extract_path):
    os.makedirs(extract_path)

try:
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Extraction successful.")
except Exception as e:
    print(f"Error: {e}")
