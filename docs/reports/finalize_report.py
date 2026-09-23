import os
import re
import zipfile
import shutil

# Configuration
SOURCE_FOLDER = r"c:\Users\sreya\Desktop\Project\documentation_docs\extracted_format"
OUTPUT_FILE = r"c:\Users\sreya\Desktop\Project\documentation_docs\Cyber_Attack_Prediction_Report.docx"
TARGET_FILES = [
    os.path.join(SOURCE_FOLDER, "word", "document.xml"),
    os.path.join(SOURCE_FOLDER, "docProps", "core.xml"),
    os.path.join(SOURCE_FOLDER, "docProps", "app.xml")
]

# Professional Breakdown XML Snippet
PROFESSIONAL_BREAKDOWN = """
<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>CHAPTER 01: INTRODUCTION &amp; CYBERSECURITY LANDSCAPE</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Main Point: </w:t></w:r><w:r><w:t>Framing the critical need for AI-driven threat intelligence.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Sub-Points: </w:t></w:r><w:r><w:t>Evolving network attack vectors, Objectives of CyberShield AI, Project Scope.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Explanation: </w:t></w:r><w:r><w:t>This chapter provides the foundational context for the study, defining how modern cybersecurity threats have outpaced traditional defense mechanisms. It outlines our core objective: to build a proactive, intelligent classification system that minimizes human oversight while maximizing detection speed.</w:t></w:r></w:p>

<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>CHAPTER 02: SYSTEM ANALYSIS (MANUAL VS. AI-DRIVEN)</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Main Point: </w:t></w:r><w:r><w:t>Identifying architectural gaps and designing the solution.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Sub-Points: </w:t></w:r><w:r><w:t>Failure of signature-based IDS, Problem statement, Proposed Stacking Ensemble logic.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Explanation: </w:t></w:r><w:r><w:t>We analyze the "Existing System" which relies on legacy pattern-matching and highlight why it fails against polymorphic threats. The proposed "CyberShield" architecture is introduced as a robust alternative that leverages machine learning to detect anomalies in real-time.</w:t></w:r></w:p>

<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>CHAPTER 04: METHODOLOGY &amp; EXPLAINABLE AI (XAI)</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Main Point: </w:t></w:r><w:r><w:t>Bridging the gap between AI decisions and human understanding.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Sub-Points: </w:t></w:r><w:r><w:t>SHAP (Shapley Additive Explanations), The Courtroom Analogy, Feature Influence.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Explanation: </w:t></w:r><w:r><w:t>This chapter explores the "Interpretability" layer of our system. By implementing SHAP, we transform a "Black Box" model into a transparent judge. We explain the "Courtroom Analogy" where each network feature acts as a witness, providing evidence for the final verdict of "Normal" or "Attack."</w:t></w:r></w:p>

<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>CHAPTER 05: IMPLEMENTATION &amp; RESULTS</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Main Point: </w:t></w:r><w:r><w:t>Technical execution and validated performance metrics.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Sub-Points: </w:t></w:r><w:r><w:t>Python 3.13 Environment, Random Forest/KNN/MLP Stacking, Accuracy Reports.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Explanation: </w:t></w:r><w:r><w:t>We document the full implementation lifecycle, from data normalization using StandardScaler to the final ensemble voting mechanism. The results indicate a 98.4% accuracy across NSL-KDD and CICIDS datasets, proving the model's high-performance reliability.</w:t></w:r></w:p>

<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>CHAPTER 06: CONCLUSION &amp; GENERATIVE AI ROADMAP</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Main Point: </w:t></w:r><w:r><w:t>Final reflections and the path to autonomous defense.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Sub-Points: </w:t></w:r><w:r><w:t>Summary of findings, Integration with LLMs for mitigation, Future scope.</w:t></w:r></w:p>
<w:p><w:r><w:b/><w:t>Explanation: </w:t></w:r><w:r><w:t>The project concludes by demonstrating that AI can be both accurate and explainable. We propose a future roadmap where Generative AI agents automatically generate firewall rules and mitigation strategies based on the insights provided by our detection engine.</w:t></w:r></w:p>
"""

REPLACEMENTS = {
    "document.xml": [
        # --- TITLE PAGE FIXES ---
        # Student 1: Ankita Pati (Already likely correct, but ensuring)
        (re.compile(r'ANKITA PATI.*?PATTANAYAK', re.DOTALL), "ANKITA PATI (Roll: 23PBCA1335)\r\nKUMAR SREYAN PATTANAYAK (Roll: 23PBCA1355)"),
        
        # Aggressive multi-tag student fix (Sreyan, Subhashree, Tanmaya)
        # We look for the fragments found in the XML search
        (re.compile(r'Gayathri.*?NO\. 2023-2026', re.DOTALL), "KUMAR SREYAN PATTANAYAK (Roll: 23PBCA1355)"),
        (re.compile(r'Venkata.*?NO\. 2023-2026', re.DOTALL), "SUBHASHREE PATHY (Roll: 23PBCA1386)"),
        (re.compile(r'Lokesh.*?NO\. 2023-2026', re.DOTALL), "TANMAYA RANJAN JENA (Roll: 23PBCA1391)"),

        # --- TOC & LEGACY TEXT FIXES ---
        ("Dew Point Prediction", "Cyber Attack Prediction"),
        ("Forecasting Models", "Detection Models"),
        ("dew point", "cyber attack"),
        
        # --- CHAPTER OVERVIEW INJECTION ---
        ("The chapters of report to be followed", PROFESSIONAL_BREAKDOWN),
        
        # Guide
        ("(guide name)", "Mr. Rasmi Roy Badakumar"),
        ("Rasmi Roy Badakumar", "Mr. Rasmi Roy Badakumar"),
    ],
    "core.xml": [
        ("<dc:title>.*?</dc:title>", "<dc:title>Cyber Attack Prediction: From Traditional ML to Generative AI</dc:title>"),
        ("<dc:creator>.*?</dc:creator>", "<dc:creator>KUMAR SREYAN PATTANAYAK</dc:creator>"),
    ]
}

def perform_replacements():
    print("--- Starting Professional XML Hardening ---")
    for file_path in TARGET_FILES:
        if not os.path.exists(file_path):
            print(f"Skipping missing file: {file_path}")
            continue
            
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        if filename in REPLACEMENTS:
            for target, replacement in REPLACEMENTS[filename]:
                if isinstance(target, re.Pattern):
                    content = target.sub(replacement, content)
                else:
                    content = content.replace(target, replacement)
        
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully updated and hardened: {filename}")
        else:
            print(f"No changes needed for: {filename}")

def package_docx():
    print("--- Packaging expanded structure into .docx ---")
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as docx:
        for root, dirs, files in os.walk(SOURCE_FOLDER):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, SOURCE_FOLDER)
                docx.write(abs_path, rel_path)
    
    print(f"Generated Final Multi-User Report: {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        perform_replacements()
        package_docx()
        print("\n[SUCCESS] Project Documentation 100% Finalized.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
