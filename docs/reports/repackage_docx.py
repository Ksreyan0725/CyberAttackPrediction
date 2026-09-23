import zipfile
import os

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, rel_path)

if __name__ == "__main__":
    extracted_dir = r"c:\Users\sreya\OneDrive\Desktop\Project\docs\extracted_format"
    output_docx = r"c:\Users\sreya\OneDrive\Desktop\Project\docs\Cyber_Attack_Prediction_Report.docx"
    
    if os.path.exists(extracted_dir):
        zip_folder(extracted_dir, output_docx)
        print(f"Successfully repackaged docx to: {output_docx}")
    else:
        print(f"Error: Extracted directory not found: {extracted_dir}")
